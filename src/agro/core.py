import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import config


def _run_command(command, cwd=None, check=True, capture_output=False, shell=False):
    """Helper to run a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            text=True,
            capture_output=capture_output,
            shell=shell,
        )
        return result
    except subprocess.CalledProcessError as e:
        cmd_str = command if isinstance(command, str) else " ".join(command)
        print(f"Error executing command: {cmd_str}", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        raise
    except FileNotFoundError:
        cmd_name = command if isinstance(command, str) else command[0]
        print(
            f"Error: Command '{cmd_name}' not found. Is it in your PATH?",
            file=sys.stderr,
        )
        raise


def make_new_tree(index, fresh_env, no_overrides, no_all_extras):
    """Creates a new git worktree with a dedicated environment."""
    tree_name = f"t{index}"
    branch_name = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
    worktree_path = Path(config.WORKTREE_DIR) / tree_name
    api_port = config.BASE_API_PORT + index
    db_port = config.DB_BASE_PORT + index
    db_container_name = f"{config.DB_CONTAINER_NAME_PREFIX}-t{index}"
    api_container_name = f"{config.API_CONTAINER_NAME_PREFIX}-t{index}"
    db_volume_name = f"{config.DB_VOLUME_NAME_PREFIX}-t{index}"
    network_name = f"app_net_t{index}"
    subnet_third_octet = 32 + index
    network_subnet = f"192.168.{subnet_third_octet}.0/24"
    network_gateway = f"192.168.{subnet_third_octet}.1"

    worktree_path.parent.mkdir(parents=True, exist_ok=True)

    if worktree_path.exists():
        raise FileExistsError(f"Worktree path '{worktree_path}' already exists.")

    print(
        f"Creating new worktree '{tree_name}' at '{worktree_path}' on branch '{branch_name}'..."
    )
    _run_command(["git", "worktree", "add", "-b", branch_name, str(worktree_path)])

    env_source_path = Path(".env.example" if fresh_env else ".env")
    env_dest_path = worktree_path / ".env"
    print(f"Copying {env_source_path} to {env_dest_path}")
    if not env_source_path.exists():
        print(
            f"Warning: Source env file '{env_source_path}' not found. Creating an empty .env file.",
            file=sys.stderr,
        )
        env_dest_path.touch()
    else:
        shutil.copy(env_source_path, env_dest_path)

    if not no_overrides:
        print(f"Adding worktree overrides to {env_dest_path}")
        with env_dest_path.open("a") as f:
            f.write("\n")
            f.write("### Worktree Overrides ---\n")
            f.write(f"API_PORT={api_port}\n")
            f.write(f"API_MAPPED_PORT={api_port}\n")
            f.write(f"DB_MAPPED_PORT={db_port}\n")
            f.write(f"DB_VOLUME_NAME={db_volume_name}\n")
            f.write(f"DB_CONTAINER_NAME={db_container_name}\n")
            f.write(f"API_CONTAINER_NAME={api_container_name}\n")
            f.write(f"NETWORK_NAME={network_name}\n")
            f.write(f"NETWORK_SUBNET={network_subnet}\n")
            f.write(f"NETWORK_GATEWAY={network_gateway}\n")
            f.write(f"FORWARDED_ALLOW_IPS={network_gateway}\n")

    print(f"Setting up Python environment in {worktree_path}...")
    _run_command(["uv", "venv"], cwd=str(worktree_path), capture_output=True)

    uv_sync_command = ["uv", "sync", "--quiet"]
    if not no_all_extras:
        uv_sync_command.append("--all-extras")
    _run_command(uv_sync_command, cwd=str(worktree_path))

    print("\n" + "🌴 New worktree created successfully.")
    print(f"   Worktree: {worktree_path}")
    print(f"   Branch: {branch_name}")
    if not no_overrides:
        print(f"   API Port: {api_port}")
        print(f"   DB Port:  {db_port}")
    print(f"To start working, run: cd {worktree_path} && source .venv/bin/activate")


def delete_tree(index):
    """Removes a worktree and its associated git branch."""
    tree_name = f"t{index}"
    branch_name = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
    worktree_path = Path(config.WORKTREE_DIR) / tree_name

    if worktree_path.is_dir() and (worktree_path / ".git").is_file():
        print(f"Removing worktree '{tree_name}' at {worktree_path}...")
        _run_command(["git", "worktree", "remove", "--force", str(worktree_path)])
    else:
        print(
            f"Info: Worktree '{worktree_path}' not found or not a valid worktree. Skipping removal."
        )

    result = _run_command(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        check=False,
    )
    if result.returncode == 0:
        print(f"Deleting branch '{branch_name}'...")
        _run_command(["git", "branch", "-D", branch_name])
    else:
        print(f"Info: Branch '{branch_name}' not found. Skipping deletion.")

    print(f"♻️  Cleanup for index {index} complete.")


def exec_agent(index, fresh_env, no_overrides, no_all_extras, task_file, agent_args):
    """Deletes, recreates, and runs a detached agent process in a worktree."""
    print(f"Attempting to remove existing worktree for index {index} (if any)...")
    try:
        delete_tree(index)
    except Exception as e:
        print(f"Could not delete tree for index {index}: {e}. Continuing...", file=sys.stderr)

    print(f"\nCreating new worktree for index {index}...")
    make_new_tree(index, fresh_env, no_overrides, no_all_extras)

    worktree_path = Path(config.WORKTREE_DIR) / f"t{index}"
    task_fn_stem = Path(task_file).stem
    base_branch_name = f"{config.WORKTREE_OUTPUT_BRANCH_PREFIX}{task_fn_stem}"
    counter = 1

    while True:
        new_branch_name = f"{base_branch_name}.{counter}"
        result = _run_command(
            ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{new_branch_name}"],
            check=False,
        )
        if result.returncode != 0:
            break
        counter += 1

    print("")
    _run_command(["git", "checkout", "-b", new_branch_name], cwd=str(worktree_path))
    print(f"🌱 Working on new branch: {new_branch_name}")
    print("")

    pid_dir = Path(".agdocs/swap")
    pid_dir.mkdir(parents=True, exist_ok=True)
    pid_file = pid_dir / f"t{index}.pid"

    print(f"Launching agent in detached mode from within {worktree_path}...")

    log_file_path = worktree_path / "maider.log"
    abs_task_file = os.path.abspath(task_file)
    command = ["maider.sh", "--yes", "-f", abs_task_file] + agent_args

    with open(log_file_path, "wb") as log_file:
        process = subprocess.Popen(
            command,
            cwd=str(worktree_path),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,  # Detach from parent
        )

    pid_file.write_text(str(process.pid))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("")
    print(f"🏃 Agent for index {index} started successfully.")
    print(f"   Worktree: {worktree_path.resolve()}")
    print(f"   Task file: {abs_task_file}")
    print(f"   Branch: {new_branch_name}")
    print(f"   Start time: {current_time}")
    print(f"   PID: {process.pid} (saved to {pid_file.resolve()})")
    print(f"   Log file: {log_file_path.resolve()}")


def muster_command(command_str, indices_str, server=False, kill_server=False):
    """Runs a command in multiple worktrees."""
    if server and kill_server:
        raise ValueError("--server and --kill-server cannot be used together.")

    try:
        indices = [int(i.strip()) for i in indices_str.split(',') if i.strip()]
    except ValueError:
        print(f"Error: Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers.", file=sys.stderr)
        raise

    use_shell = False
    final_command_str = command_str

    if kill_server:
        final_command_str = "kill $(cat server.pid) && rm -f server.pid server.log"
        use_shell = True
    elif server:
        if not command_str.strip():
            raise ValueError("Empty command provided for --server.")
        final_command_str = f"{command_str} > server.log 2>&1 & echo $! > server.pid"
        use_shell = True

    if use_shell:
        command = final_command_str
    else:
        command = shlex.split(final_command_str)
        if not command:
            raise ValueError("Empty command provided.")

    for index in indices:
        tree_name = f"t{index}"
        worktree_path = Path(config.WORKTREE_DIR) / tree_name

        if not worktree_path.is_dir():
            print(f"Warning: Worktree t{index} at '{worktree_path}' not found. Skipping.", file=sys.stderr)
            continue

        print(f"\n--- Running command in t{index} ({worktree_path}) ---")
        print(f"$ {final_command_str}")
        try:
            _run_command(command, cwd=str(worktree_path), shell=use_shell)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # _run_command already prints details.
            print(f"--- Command failed in t{index}. Continuing... ---", file=sys.stderr)
            continue


def grab_branch(branch_name):
    """
    Checks out a branch. If the branch is checked out in another worktree,
    creates a copy of it and checks out the copy.
    """
    print(f"Attempting to checkout branch '{branch_name}'...")
    try:
        # We capture output here to inspect stderr on failure
        _run_command(["git", "checkout", branch_name], capture_output=True)
        print(f"Successfully checked out branch '{branch_name}'.")
    except subprocess.CalledProcessError as e:
        if e.stderr and "is already checked out at" in e.stderr:
            copy_branch_name = f"{branch_name}.copy"
            print(f"Branch '{branch_name}' is in use by another worktree.")
            print(f"Creating/updating copy '{copy_branch_name}' and checking it out.")
            _run_command(["git", "branch", "-f", copy_branch_name, branch_name])
            _run_command(["git", "checkout", copy_branch_name])
            print(f"Successfully checked out branch '{copy_branch_name}'.")
        else:
            # Re-raise if it's a different error
            raise


def fade_branches(pattern):
    """Deletes local git branches matching a pattern after user confirmation."""
    print(f"Searching for branches matching pattern: '{pattern}'")

    result = _run_command(["git", "branch"], capture_output=True, check=True)
    all_branches_raw = result.stdout.strip().split('\n')

    branches_to_delete = []
    for line in all_branches_raw:
        branch_name = line.lstrip(' *+')
        if re.search(pattern, branch_name):
            if line.startswith('* '):
                print(f"Warning: Skipping currently checked out branch '{branch_name}'", file=sys.stderr)
                continue
            branches_to_delete.append(branch_name)

    if not branches_to_delete:
        print("No branches found matching the pattern to delete.")
        return

    print("\n--- Dry Run ---")
    print("The following branches would be deleted:")
    for branch in branches_to_delete:
        print(f"  {branch}")
    print("--- End Dry Run ---\n")

    try:
        confirm = input(f"Delete these {len(branches_to_delete)} branches? (Y/n): ")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")
        return

    if confirm.lower() != 'y':
        print("Operation cancelled by user.")
        return

    print("\nDeleting branches...")
    deleted_count = 0
    failed_count = 0
    for branch in branches_to_delete:
        result = _run_command(["git", "branch", "-D", branch], capture_output=True, check=False)
        if result.returncode == 0:
            print(f"Deleted branch '{branch}'.")
            deleted_count += 1
        else:
            print(f"Failed to delete branch '{branch}':", file=sys.stderr)
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
            failed_count += 1

    print(f"\nFade complete. Deleted {deleted_count} branches, {failed_count} failed.")


def surrender(indices_str=None):
    """Kills running agent processes associated with worktrees."""
    pid_dir = Path(".agdocs/swap")
    if not pid_dir.is_dir():
        print("No agent processes seem to be running (PID directory not found).")
        return

    target_indices = []
    if not indices_str or indices_str.lower() == 'all':
        for pid_file in sorted(pid_dir.glob("t*.pid")):
            match = re.match(r"t(\d+)\.pid", pid_file.name)
            if match:
                target_indices.append(int(match.group(1)))
        if not target_indices:
            print("No PID files found in .agdocs/swap.")
            return
    else:
        try:
            target_indices = [int(i.strip()) for i in indices_str.split(',') if i.strip()]
        except ValueError:
            print(f"Error: Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers.", file=sys.stderr)
            raise

    procs_to_kill = []
    print("--- Dry Run ---")
    print("Checking for running agent processes...")
    for index in sorted(target_indices):
        pid_file = pid_dir / f"t{index}.pid"
        if not pid_file.exists():
            continue

        try:
            pid_str = pid_file.read_text().strip()
            if not pid_str:
                continue
            pid = int(pid_str)
        except (ValueError, IOError) as e:
            print(f"Warning: Could not read PID for index {index} from {pid_file}: {e}", file=sys.stderr)
            continue

        # Check if process is running
        result = _run_command(["ps", "-p", str(pid)], check=False, capture_output=True)
        if result.returncode == 0:
            procs_to_kill.append({'index': index, 'pid': pid, 'pid_file': pid_file})
            print(f"  - Found running process for t{index}: PID {pid}")

    if not procs_to_kill:
        print("\nNo active agent processes found to surrender.")
        return

    print("--- End Dry Run ---\n")

    try:
        confirm = input(f"Surrender and kill these {len(procs_to_kill)} processes? (Y/n): ")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")
        return

    if confirm.lower() != 'y':
        print("Operation cancelled by user.")
        return

    print("\nProceeding with termination...")
    killed_count = 0
    failed_count = 0
    for proc in procs_to_kill:
        index = proc['index']
        pid = proc['pid']
        pid_file = proc['pid_file']
        print(f"Killing process for t{index} (PID {pid})...")
        try:
            # Using kill command to be safe and simple. It sends SIGTERM by default.
            _run_command(["kill", str(pid)], check=True, capture_output=True)
            print(f"  - Process {pid} terminated.")
            killed_count += 1
        except subprocess.CalledProcessError:
            # Check if it failed because the process was already gone
            result = _run_command(["ps", "-p", str(pid)], check=False, capture_output=True)
            if result.returncode != 0:
                print(f"  - Process {pid} was already gone.")
                killed_count += 1 # Count it as a success for cleanup purposes
            else:
                print(f"  - Failed to kill process {pid}.", file=sys.stderr)
                failed_count += 1
                continue # Don't remove PID file if kill failed and process is running

        # Clean up pid file
        try:
            pid_file.unlink()
            print(f"  - Removed PID file {pid_file}.")
        except OSError as e:
            print(f"  - Warning: Could not remove PID file {pid_file}: {e}", file=sys.stderr)

    print(f"\nSurrender complete. Terminated {killed_count} processes, {failed_count} failed.")
