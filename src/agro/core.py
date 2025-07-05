import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import config

logger = logging.getLogger(__name__)


def _run_command(
    command,
    cwd=None,
    check=True,
    capture_output=False,
    shell=False,
    show_cmd_output=False,
):
    """Helper to run a shell command."""
    cmd_str = command if isinstance(command, str) else shlex.join(command)
    logger.debug(f"Running command in '{cwd or '.'}': $ {cmd_str}")

    # Capture output to suppress it, unless show_cmd_output is True
    do_capture = capture_output or not show_cmd_output

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            text=True,
            capture_output=do_capture,
            shell=shell,
        )
        return result
    except subprocess.CalledProcessError as e:
        cmd_str = command if isinstance(command, str) else shlex.join(command)
        logger.error(f"Error executing command: {cmd_str}")
        # If output was captured, it's in the exception.
        if e.stdout:
            logger.error(f"STDOUT:\n{e.stdout.strip()}")
        if e.stderr:
            logger.error(f"STDERR:\n{e.stderr.strip()}")
        raise
    except FileNotFoundError:
        cmd_name = command if isinstance(command, str) else command[0]
        logger.error(f"Error: Command '{cmd_name}' not found. Is it in your PATH?")
        raise


def make_new_tree(index, fresh_env, no_overrides, no_all_extras, show_cmd_output=False):
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

    # Get the current commit SHA before creating the worktree
    sha_result = _run_command(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        show_cmd_output=show_cmd_output,
    )
    initial_sha = sha_result.stdout.strip()

    # Ensure the worktree directory is in .gitignore
    worktree_root_dir_str = config.WORKTREE_DIR
    result = _run_command(
        ["git", "check-ignore", "-q", worktree_root_dir_str],
        check=False,
        show_cmd_output=show_cmd_output,
    )
    if result.returncode == 1:  # Not ignored
        gitignore_path = Path(".gitignore")
        # Ensure we add a clean path with a trailing slash
        entry = worktree_root_dir_str.lstrip("./")
        if not entry.endswith("/"):
            entry += "/"

        logger.info(f"Adding '{entry}' to {gitignore_path}...")
        with gitignore_path.open("a") as f:
            f.write(f"\n# Agro worktrees\n{entry}\n")

    if worktree_path.exists():
        raise FileExistsError(f"Worktree path '{worktree_path}' already exists.")

    logger.debug(
        f"Creating new worktree '{tree_name}' at '{worktree_path}' on branch '{branch_name}'..."
    )
    _run_command(
        ["git", "worktree", "add", "-b", branch_name, str(worktree_path)],
        show_cmd_output=show_cmd_output,
    )

    env_source_path = Path(".env.example" if fresh_env else ".env")
    env_dest_path = worktree_path / ".env"

    env_file_created = False
    if env_source_path.exists():
        logger.debug(f"Copying {env_source_path} to {env_dest_path}")
        shutil.copy(env_source_path, env_dest_path)
        env_file_created = True
    elif Path(".env").exists() or Path(".env.example").exists():
        logger.warning(
            f"Source env file '{env_source_path}' not found. Creating an empty .env file."
        )
        env_dest_path.touch()
        env_file_created = True
    else:
        logger.warning(
            "Neither .env nor .env.example found in root. No .env file will be created."
        )

    if not no_overrides and env_file_created:
        logger.debug(f"Adding worktree overrides to {env_dest_path}")
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

    logger.debug(f"Setting up Python environment in {worktree_path}...")
    _run_command(
        ["uv", "venv"],
        cwd=str(worktree_path),
        capture_output=True,
        show_cmd_output=show_cmd_output,
    )

    uv_sync_command = ["uv", "sync", "--quiet"]
    if not no_all_extras:
        uv_sync_command.append("--all-extras")
    _run_command(uv_sync_command, cwd=str(worktree_path), show_cmd_output=show_cmd_output)

    logger.debug("\n" + "🌴 New worktree created successfully.")
    logger.debug(f"   Worktree: {worktree_path}")
    logger.debug(f"   Branch: {branch_name}")
    if not no_overrides and env_file_created:
        logger.debug(f"   API Port: {api_port}")
        logger.debug(f"   DB Port:  {db_port}")

    return initial_sha


def delete_tree(indices_str=None, all_flag=False, show_cmd_output=False):
    """Removes one or all worktrees and their associated git branches."""
    indices_to_process = []

    if all_flag:
        worktree_dir = Path(config.WORKTREE_DIR)
        if not worktree_dir.is_dir():
            logger.warning(f"Worktree directory '{worktree_dir}' not found.")
            return

        indices_to_delete = []
        for p in worktree_dir.iterdir():
            if p.is_dir() and re.match(r"^t\d+$", p.name):
                try:
                    index_str = p.name[1:]
                    indices_to_delete.append(int(index_str))
                except ValueError:
                    continue

        if not indices_to_delete:
            logger.warning("No worktrees found to delete.")
            return

        logger.info("The following worktrees will be deleted:")
        for i in sorted(indices_to_delete):
            logger.info(f"  - t{i}")
        logger.info("")

        try:
            confirm = input(
                f"Delete these {len(indices_to_delete)} worktrees? [Y/n]: "
            )
        except (EOFError, KeyboardInterrupt):
            logger.warning("\nOperation cancelled.")
            return

        if confirm.lower() not in ("y", ""):
            logger.warning("Operation cancelled by user.")
            return

        logger.info("\nDeleting worktrees...")
        indices_to_process = sorted(indices_to_delete)
    elif indices_str is not None:
        try:
            indices_to_process = [
                int(i.strip()) for i in indices_str.split(",") if i.strip()
            ]
        except ValueError:
            logger.error(
                f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
            )
            raise

        if not indices_to_process:
            logger.info("No worktrees to delete.")
            return

        if len(indices_to_process) > 1:
            logger.info("The following worktrees will be deleted:")
            for i in sorted(indices_to_process):
                logger.info(f"  - t{i}")
            logger.info("")

            try:
                confirm = input(
                    f"Delete these {len(indices_to_process)} worktrees? [Y/n]: "
                )
            except (EOFError, KeyboardInterrupt):
                logger.warning("\nOperation cancelled.")
                return

            if confirm.lower() not in ("y", ""):
                logger.warning("Operation cancelled by user.")
                return

            logger.info("\nDeleting worktrees...")
    else:
        # This case should be prevented by the CLI argument parsing
        logger.error("No index specified for deletion.")
        return

    for i in indices_to_process:
        tree_name = f"t{i}"
        branch_name = f"{config.WORKTREE_BRANCH_PREFIX}{i}"
        worktree_path = Path(config.WORKTREE_DIR) / tree_name

        if worktree_path.is_dir() and (worktree_path / ".git").is_file():
            logger.debug(f"Removing worktree '{tree_name}' at {worktree_path}...")
            _run_command(
                ["git", "worktree", "remove", "--force", str(worktree_path)],
                show_cmd_output=show_cmd_output,
            )
        else:
            logger.warning(
                f"Worktree '{worktree_path}' not found or not a valid worktree. Skipping removal."
            )

        result = _run_command(
            ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
            check=False,
            show_cmd_output=show_cmd_output,
        )
        if result.returncode == 0:
            logger.debug(f"Deleting branch '{branch_name}'...")
            _run_command(
                ["git", "branch", "-D", branch_name], show_cmd_output=show_cmd_output
            )
        else:
            logger.warning(f"Branch '{branch_name}' not found. Skipping deletion.")

        logger.info(f"♻️  Cleanup for index {i} complete.")


def exec_agent(
    task_file,
    fresh_env,
    no_overrides,
    no_all_extras,
    agent_args,
    indices_str=None,
    num_trees=None,
    show_cmd_output=False,
):
    """Deletes, recreates, and runs detached agent processes in worktrees."""
    task_path = Path(task_file)
    if not task_path.is_file():
        logger.error(f"Task file not found: {task_file}")
        raise FileNotFoundError(f"Task file not found: {task_file}")

    if task_path.stat().st_size == 0:
        logger.error(f"Task file is empty: {task_file}")
        raise ValueError(f"Task file is empty: {task_file}")

    indices_to_process = []
    if indices_str:
        try:
            indices_to_process = [
                int(i.strip()) for i in indices_str.split(",") if i.strip()
            ]
        except ValueError:
            logger.error(
                f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
            )
            raise
    else:
        num_to_create = num_trees if num_trees is not None else 1

        worktree_dir = Path(config.WORKTREE_DIR)
        existing_indices = set()
        if worktree_dir.is_dir():
            for p in worktree_dir.iterdir():
                if p.is_dir() and re.match(r"^t\d+$", p.name):
                    try:
                        existing_indices.add(int(p.name[1:]))
                    except ValueError:
                        continue

        new_indices = []
        next_index = 1
        while len(new_indices) < num_to_create:
            if next_index not in existing_indices:
                new_indices.append(next_index)
            next_index += 1
        indices_to_process = new_indices

        if not indices_to_process and num_trees is not None:
            logger.debug("Number of trees is 0, no worktrees will be created.")
        elif num_trees is None:
            if not indices_to_process:
                logger.warning("Could not determine next available index.")
            else:
                logger.debug(f"No indices provided. Using next available index: {indices_to_process[0]}")
        elif num_trees is not None:
            logger.debug(
                f"Using next {num_trees} available indices: {', '.join(map(str, indices_to_process))}"
            )

    for index in indices_to_process:
        logger.debug(f"\n--- Processing worktree for index {index} ---")
        logger.debug(
            f"Attempting to remove existing worktree for index {index} (if any)..."
        )
        try:
            delete_tree(str(index), show_cmd_output=show_cmd_output)
        except Exception as e:
            logger.warning(
                f"Could not delete tree for index {index}: {e}. Continuing..."
            )

        logger.debug(f"\nCreating new worktree for index {index}...")
        initial_sha = make_new_tree(
            index, fresh_env, no_overrides, no_all_extras, show_cmd_output
        )

        worktree_path = Path(config.WORKTREE_DIR) / f"t{index}"
        task_fn_stem = Path(task_file).stem
        base_branch_name = f"{config.WORKTREE_OUTPUT_BRANCH_PREFIX}{task_fn_stem}"
        counter = 1

        while True:
            new_branch_name = f"{base_branch_name}.{counter}"
            result = _run_command(
                [
                    "git",
                    "rev-parse",
                    "--verify",
                    "--quiet",
                    f"refs/heads/{new_branch_name}",
                ],
                check=False,
                show_cmd_output=show_cmd_output,
            )
            if result.returncode != 0:
                break
            counter += 1

        _run_command(
            ["git", "checkout", "-b", new_branch_name],
            cwd=str(worktree_path),
            show_cmd_output=show_cmd_output,
        )
        logger.debug(f"🌱 Working on new branch: {new_branch_name}")

        pid_dir = Path(".agdocs/swap")
        pid_dir.mkdir(parents=True, exist_ok=True)
        pid_file = pid_dir / f"t{index}.pid"

        logger.debug(f"Launching agent in detached mode from within {worktree_path}...")

        log_file_path = worktree_path / "maider.log"
        abs_task_file = os.path.abspath(task_file)
        command = [
            "maider.sh",
            "--yes",
            "-f",
            abs_task_file,
            "--no-check-update",
            "--no-attribute-author",
            "--no-attribute-committer",
            "--no-attribute-co-authored-by",
        ] + agent_args

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
        logger.info("")
        logger.info(f"🏃 Agent for index {index} started successfully.")
        logger.info(f"   Worktree: {worktree_path.resolve()}")
        logger.info(f"   Task file: {abs_task_file}")
        logger.info(f"   Branch: {new_branch_name}")
        logger.info(f"   Initial SHA: {initial_sha}")
        logger.info(f"   Start time: {current_time}")
        logger.info(f"   PID: {process.pid} (saved to {pid_file.resolve()})")
        logger.info(f"   Log file: {log_file_path.resolve()}")


def muster_command(
    command_str, indices_str, server=False, kill_server=False, show_cmd_output=False
):
    """Runs a command in multiple worktrees."""
    if server and kill_server:
        raise ValueError("--server and --kill-server cannot be used together.")

    try:
        indices = [int(i.strip()) for i in indices_str.split(",") if i.strip()]
    except ValueError:
        logger.error(
            f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
        )
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
            logger.warning(
                f"Worktree t{index} at '{worktree_path}' not found. Skipping."
            )
            continue

        logger.info(f"\n--- Running command in t{index} ({worktree_path}) ---")
        logger.info(f"$ {final_command_str}")
        try:
            _run_command(
                command,
                cwd=str(worktree_path),
                shell=use_shell,
                show_cmd_output=show_cmd_output,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # _run_command already prints details.
            logger.error(f"--- Command failed in t{index}. Continuing... ---")
            continue


def grab_branch(branch_name, show_cmd_output=False):
    """
    Checks out a branch. If the branch is checked out in another worktree,
    creates a copy of it and checks out the copy.
    """
    logger.info(f"Attempting to checkout branch '{branch_name}'...")
    try:
        # We capture output here to inspect stderr on failure
        _run_command(
            ["git", "checkout", branch_name],
            capture_output=True,
            show_cmd_output=show_cmd_output,
        )
        logger.info(f"Successfully checked out branch '{branch_name}'.")
    except subprocess.CalledProcessError as e:
        if e.stderr and "is already checked out at" in e.stderr:
            copy_branch_name = f"{branch_name}.copy"
            logger.warning(f"Branch '{branch_name}' is in use by another worktree.")
            logger.debug(
                f"Creating/updating copy '{copy_branch_name}' and checking it out."
            )
            _run_command(
                ["git", "branch", "-f", copy_branch_name, branch_name],
                show_cmd_output=show_cmd_output,
            )
            _run_command(
                ["git", "checkout", copy_branch_name], show_cmd_output=show_cmd_output
            )
            logger.info(f"Successfully checked out branch '{copy_branch_name}'.")
        else:
            # Re-raise if it's a different error
            raise


def fade_branches(pattern, show_cmd_output=False):
    """Deletes local git branches matching a pattern after user confirmation."""
    logger.info(f"Searching for branches matching pattern: '{pattern}'")

    result = _run_command(
        ["git", "branch"],
        capture_output=True,
        check=True,
        show_cmd_output=show_cmd_output,
    )
    all_branches_raw = result.stdout.strip().split("\n")

    branches_to_delete = []
    for line in all_branches_raw:
        branch_name = line.lstrip(" *+")
        if re.search(pattern, branch_name):
            if line.startswith("* "):
                logger.warning(
                    f"Skipping currently checked out branch '{branch_name}'"
                )
                continue
            branches_to_delete.append(branch_name)

    if not branches_to_delete:
        logger.info("No branches found matching the pattern to delete.")
        return

    logger.info("\n--- Dry Run ---")
    logger.info("The following branches would be deleted:")
    for branch in branches_to_delete:
        logger.info(f"  {branch}")
    logger.info("--- End Dry Run ---\n")

    try:
        confirm = input(f"Delete these {len(branches_to_delete)} branches? [Y/n]: ")
    except (EOFError, KeyboardInterrupt):
        logger.warning("\nOperation cancelled.")
        return

    if confirm.lower() not in ("y", ""):
        logger.warning("Operation cancelled by user.")
        return

    logger.info("\nDeleting branches...")
    deleted_count = 0
    failed_count = 0
    for branch in branches_to_delete:
        result = _run_command(
            ["git", "branch", "-D", branch],
            capture_output=True,
            check=False,
            show_cmd_output=show_cmd_output,
        )
        if result.returncode == 0:
            logger.info(f"Deleted branch '{branch}'.")
            deleted_count += 1
        else:
            logger.error(f"Failed to delete branch '{branch}':")
            if result.stderr:
                logger.error(result.stderr.strip())
            failed_count += 1

    logger.info(
        f"\nFade complete. Deleted {deleted_count} branches, {failed_count} failed."
    )


def surrender(indices_str=None, show_cmd_output=False):
    """Kills running agent processes associated with worktrees."""
    pid_dir = Path(".agdocs/swap")
    if not pid_dir.is_dir():
        logger.info("No agent processes seem to be running (PID directory not found).")
        return

    target_indices = []
    if not indices_str or indices_str.lower() == 'all':
        for pid_file in sorted(pid_dir.glob("t*.pid")):
            match = re.match(r"t(\d+)\.pid", pid_file.name)
            if match:
                target_indices.append(int(match.group(1)))
        if not target_indices:
            logger.info("No PID files found in .agdocs/swap.")
            return
    else:
        try:
            target_indices = [
                int(i.strip()) for i in indices_str.split(",") if i.strip()
            ]
        except ValueError:
            logger.error(
                f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
            )
            raise

    procs_to_kill = []
    logger.info("--- Dry Run ---")
    logger.info("Checking for running agent processes...")
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
            logger.warning(
                f"Could not read PID for index {index} from {pid_file}: {e}"
            )
            continue

        # Check if process is running
        result = _run_command(
            ["ps", "-p", str(pid)],
            check=False,
            capture_output=True,
            show_cmd_output=show_cmd_output,
        )
        if result.returncode == 0:
            procs_to_kill.append({"index": index, "pid": pid, "pid_file": pid_file})
            logger.info(f"  - Found running process for t{index}: PID {pid}")

    if not procs_to_kill:
        logger.info("\nNo active agent processes found to surrender.")
        return

    logger.info("--- End Dry Run ---\n")

    try:
        confirm = input(
            f"Surrender and kill these {len(procs_to_kill)} processes? [Y/n]: "
        )
    except (EOFError, KeyboardInterrupt):
        logger.warning("\nOperation cancelled.")
        return

    if confirm.lower() not in ("y", ""):
        logger.warning("Operation cancelled by user.")
        return

    logger.info("\nProceeding with termination...")
    killed_count = 0
    failed_count = 0
    for proc in procs_to_kill:
        index = proc["index"]
        pid = proc["pid"]
        pid_file = proc["pid_file"]
        logger.info(f"Killing process for t{index} (PID {pid})...")
        try:
            # Using kill command to be safe and simple. It sends SIGTERM by default.
            _run_command(
                ["kill", str(pid)],
                check=True,
                capture_output=True,
                show_cmd_output=show_cmd_output,
            )
            logger.info(f"  - Process {pid} terminated.")
            killed_count += 1
        except subprocess.CalledProcessError:
            # Check if it failed because the process was already gone
            result = _run_command(
                ["ps", "-p", str(pid)],
                check=False,
                capture_output=True,
                show_cmd_output=show_cmd_output,
            )
            if result.returncode != 0:
                logger.info(f"  - Process {pid} was already gone.")
                killed_count += 1  # Count it as a success for cleanup purposes
            else:
                logger.error(f"  - Failed to kill process {pid}.")
                failed_count += 1
                continue  # Don't remove PID file if kill failed and process is running

        # Clean up pid file
        try:
            pid_file.unlink()
            logger.info(f"  - Removed PID file {pid_file}.")
        except OSError as e:
            logger.warning(f"  - Could not remove PID file {pid_file}: {e}")

    logger.info(
        f"\nSurrender complete. Terminated {killed_count} processes, {failed_count} failed."
    )
