import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import config


def _run_command(command, cwd=None, check=True, capture_output=False):
    """Helper to run a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            text=True,
            capture_output=capture_output,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        raise
    except FileNotFoundError:
        print(
            f"Error: Command '{command[0]}' not found. Is it in your PATH?",
            file=sys.stderr,
        )
        raise


def make_new_tree(index, fresh_env, no_overrides):
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
    _run_command(["uv", "sync", "--quiet"], cwd=str(worktree_path))

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


def exec_agent(index, fresh_env, no_overrides, task_file, agent_args):
    """Deletes, recreates, and runs a detached agent process in a worktree."""
    print(f"Attempting to remove existing worktree for index {index} (if any)...")
    try:
        delete_tree(index)
    except Exception as e:
        print(f"Could not delete tree for index {index}: {e}. Continuing...", file=sys.stderr)

    print(f"\nCreating new worktree for index {index}...")
    make_new_tree(index, fresh_env, no_overrides)

    worktree_path = Path(config.WORKTREE_DIR) / f"t{index}"
    task_fn_stem = Path(task_file).stem
    base_branch_name = f"{config.WORKTREE_OUTPUT_BRANCH_PREFIX}{task_fn_stem}"
    new_branch_name = base_branch_name
    counter = 1

    while True:
        result = _run_command(
            ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{new_branch_name}"],
            check=False,
        )
        if result.returncode != 0:
            break
        new_branch_name = f"{base_branch_name}.{counter}"
        counter += 1

    print("")
    _run_command(["git", "checkout", "-b", new_branch_name], cwd=str(worktree_path))
    print(f"🌱 Working on new branch: {new_branch_name}")
    print("")

    pid_dir = Path(".ag_docs/swap")
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
