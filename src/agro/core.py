import fnmatch
import json
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


def find_task_file(file_str: str) -> Path | None:
    """
    Fuzzy search for a task file.
    Checks for existence as-is, with .md, and in specs dir.
    """
    p = Path(file_str)
    if p.is_file():
        return p

    if not file_str.endswith(".md"):
        p_md = Path(f"{file_str}.md")
        if p_md.is_file():
            return p_md

    specs_dir = Path(config.AGDOCS_DIR) / "specs"
    if specs_dir.is_dir():
        spec_p = specs_dir / file_str
        if spec_p.is_file():
            return spec_p

        if not file_str.endswith(".md"):
            spec_p_md = specs_dir / f"{file_str}.md"
            if spec_p_md.is_file():
                return spec_p_md

    return None


def find_most_recent_task_file() -> Path | None:
    """Finds the most recently modified .md file in the specs directory."""
    specs_dir = Path(config.AGDOCS_DIR) / "specs"
    if not specs_dir.is_dir():
        return None

    md_files = list(specs_dir.glob("*.md"))
    if not md_files:
        return None

    latest_file = max(md_files, key=lambda p: p.stat().st_mtime)
    return latest_file


def _get_all_branches(show_cmd_output=False) -> list[str]:
    """Retrieves a list of all local branch names."""
    result = _run_command(
        ["git", "branch", "--format=%(refname:short)"],
        capture_output=True,
        check=True,
        show_cmd_output=show_cmd_output,
    )
    return result.stdout.strip().split("\n") if result.stdout else []


def _expand_branch_pattern(pattern: str) -> list[str]:
    """
    Expands a branch pattern with brace expressions into a list of concrete names.
    e.g., 'feature/branch.{1-3,5}' -> ['feature/branch.1', 'feature/branch.2', 'feature/branch.3', 'feature/branch.5']
    """
    match = re.search(r"\{([^}]+)\}", pattern)
    if not match:
        return [pattern]

    prefix = pattern[: match.start()]
    suffix = pattern[match.end() :]
    content = match.group(1)

    if not content.strip():  # Handles {} and { }
        return []

    numbers = set()
    parts = content.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                start_str, end_str = part.split("-", 1)
                start, end = int(start_str), int(end_str)
                if start > end:
                    continue
                numbers.update(range(start, end + 1))
            except ValueError:
                raise ValueError(f"Invalid range in pattern: '{part}'")
        else:
            try:
                numbers.add(int(part))
            except ValueError:
                raise ValueError(f"Invalid number in pattern: '{part}'")

    return [f"{prefix}{num}{suffix}" for num in sorted(list(numbers))]


def _get_matching_branches(pattern: str, show_cmd_output=False) -> list[str]:
    """
    Finds branches matching a given pattern.
    - Expands brace notation like {1-3,5}.
    - If no brace notation and no glob chars, performs an exact match, falling back to prefix match.
    - Allows user to provide their own glob patterns.
    """
    all_branches = _get_all_branches(show_cmd_output)

    try:
        expanded_patterns = _expand_branch_pattern(pattern)
    except ValueError as e:
        logger.error(f"Pattern error: {e}")
        return []

    if "{" in pattern:
        return sorted([b for b in all_branches if b in expanded_patterns])

    plain_pattern = expanded_patterns[0]

    if plain_pattern in all_branches:
        return [plain_pattern]

    if any(c in plain_pattern for c in "*?[]"):
        return sorted(fnmatch.filter(all_branches, plain_pattern))

    return sorted(fnmatch.filter(all_branches, f"{plain_pattern}*"))


def _get_config_template():
    """Returns the content for the default agro.conf.yml."""

    # Format ENV_SETUP_CMDS
    env_setup_cmds_lines = ["# ENV_SETUP_CMDS:"]
    for cmd in config.DEFAULTS.get("ENV_SETUP_CMDS", []):
        env_setup_cmds_lines.append(f"#   - {json.dumps(cmd)}")
    env_setup_cmds_str = "\n".join(env_setup_cmds_lines)

    # Format AGENT_CONFIG
    agent_config_lines = ["# AGENT_CONFIG:"]
    for agent, settings in config.DEFAULTS.get("AGENT_CONFIG", {}).items():
        agent_config_lines.append(f"#   {agent}:")
        for key, value in settings.items():
            agent_config_lines.append(f"#     {key}: {json.dumps(value)}")
    agent_config_str = "\n".join(agent_config_lines)

    # Format AGENT_TIMEOUTS
    agent_timeouts_lines = ["# AGENT_TIMEOUTS:"]
    for agent, timeout in config.DEFAULTS.get("AGENT_TIMEOUTS", {}).items():
        agent_timeouts_lines.append(f"#   {agent}: {timeout}")
    agent_timeouts_str = "\n".join(agent_timeouts_lines)

    # Format MUSTER_COMMON_CMDS
    muster_common_cmds_lines = ["# MUSTER_COMMON_CMDS:"]
    for key, data in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
        if isinstance(data, dict):
            muster_common_cmds_lines.append(f"#   {key}:")
            muster_common_cmds_lines.append(f'#     cmd: {json.dumps(data.get("cmd"))}')
            if "timeout" in data:
                timeout_val = "null" if data["timeout"] is None else data["timeout"]
                muster_common_cmds_lines.append(f"#     timeout: {timeout_val}")
        else: # old format for robustness
            muster_common_cmds_lines.append(f"#   {key}: {json.dumps(data)}")
    muster_common_cmds_str = "\n".join(muster_common_cmds_lines)

    return f"""# Agro Configuration File
#
# This file allows you to customize the behavior of Agro.
# Uncomment and modify the settings below to override the defaults.

# --- General Paths ---

# Directory for storing private project documentation and specifications.
# AGDOCS_DIR: {config.DEFAULTS['AGDOCS_DIR']}

# Directory for storing public project documentation.
# PUBLIC_AGDOCS_DIR: {config.DEFAULTS['PUBLIC_AGDOCS_DIR']}

# Directory where git worktrees will be created.
# WORKTREE_DIR: {config.DEFAULTS['WORKTREE_DIR']}


# --- Branching ---

# Prefix for branches created for worktrees. E.g., 'tree/t1', 'tree/t2'.
# WORKTREE_BRANCH_PREFIX: {config.DEFAULTS['WORKTREE_BRANCH_PREFIX']}

# Prefix for branches created when an agent outputs changes.
# WORKTREE_OUTPUT_BRANCH_PREFIX: {config.DEFAULTS['WORKTREE_OUTPUT_BRANCH_PREFIX']}


# --- Environment Replication (for containerized apps) ---

# Base port for the API service in worktrees. Each worktree gets a unique port.
# BASE_API_PORT: {config.DEFAULTS['BASE_API_PORT']}

# --- Python Environment ---

# Commands to set up the Python environment in a new worktree.
# For example, to install all optional dependency groups with uv:
{env_setup_cmds_str}


# --- Agent Execution ---

# Default command to execute for 'agro exec'.
# EXEC_CMD_DEFAULT: {config.DEFAULTS['EXEC_CMD_DEFAULT']}

# The type of agent being used. Determines how built-in flags are passed.
# Supported values: "aider", "claude", "gemini".
# AGENT_TYPE: {config.DEFAULTS['AGENT_TYPE']}

# Agent-specific configuration.
{agent_config_str}

# Agent-specific timeout settings in seconds.
# A value of 0 means no timeout is applied, overriding any default.
{agent_timeouts_str}

# Default command to open spec files with 'agro task'.
# AGRO_EDITOR_CMD: {config.DEFAULTS['AGRO_EDITOR_CMD']}


# --- Muster ---

# Default timeout in seconds for commands run with 'agro muster'.
# A value of 0 or null means no timeout.
# MUSTER_DEFAULT_TIMEOUT: {config.DEFAULTS['MUSTER_DEFAULT_TIMEOUT']}

# Pre-defined commands for 'agro muster -c'.
{muster_common_cmds_str}
"""


def init_project(conf_only=False):
    """Initializes the .agdocs directory structure."""
    agdocs_dir = Path(config.AGDOCS_DIR)

    def ensure_agdocs_in_gitignore():
        # Add .agdocs to root .gitignore if not already present
        result = _run_command(
            ["git", "check-ignore", "-q", str(agdocs_dir)],
            check=False,
        )
        if result.returncode == 1:  # Not ignored
            root_gitignore_path = Path(".gitignore")
            entry = f"{agdocs_dir}/"
            logger.info(f"Adding '{entry}' to {root_gitignore_path}...")
            with root_gitignore_path.open("a") as f:
                f.write(f"\n# Agro project directory\n{entry}\n")

    conf_dir = agdocs_dir / "conf"
    config_file_path = conf_dir / "agro.conf.yml"

    if conf_only:
        if config_file_path.exists():
            raise FileExistsError(f"Config file already exists at '{config_file_path}'.")

        logger.debug(f"Generating config file at '{config_file_path}'...")
        conf_dir.mkdir(parents=True, exist_ok=True)
        config_file_path.write_text(_get_config_template())
        ensure_agdocs_in_gitignore()
        logger.info(f"✅ Config file created successfully: {config_file_path}")
        return

    if agdocs_dir.exists():
        logger.warning(f"'{agdocs_dir}' directory already exists. Skipping initialization.")
        return

    logger.debug(f"Initializing agro project structure in '{agdocs_dir}'...")

    agdocs_dir.mkdir()
    (agdocs_dir / "specs").mkdir()
    (agdocs_dir / "swap").mkdir()
    guides_dir = agdocs_dir / "guides"
    guides_dir.mkdir()
    (guides_dir / "GUIDE.md").write_text(
        "# Agent Guide\n\nThis file provides guidance and conventions for the AI agent.\n"
    )
    conf_dir.mkdir()

    config_file_path.write_text(_get_config_template())

    gitignore_path = agdocs_dir / ".gitignore"
    gitignore_path.write_text("swap/\n")

    ensure_agdocs_in_gitignore()

    logger.info(f"✅ Project initialized successfully in: {str(agdocs_dir)}")
    logger.debug(f"Created: {agdocs_dir}/")
    logger.debug(f"Created: {agdocs_dir}/specs/")
    logger.debug(f"Created: {agdocs_dir}/swap/")
    logger.debug(f"Created: {agdocs_dir}/guides/")
    logger.debug(f"Created: {agdocs_dir}/guides/GUIDE.md")
    logger.debug(f"Created: {agdocs_dir}/conf/")
    logger.debug(f"Created: {agdocs_dir}/conf/agro.conf.yml")
    logger.debug(f"Created: {agdocs_dir}/.gitignore")


def setup_completions(mode, show_cmd_output=False):
    """Sets up shell completions for agro."""
    shell = os.environ.get("SHELL", "")
    if "bash" not in shell:
        logger.error("Shell is not bash. Completions are only supported for bash.")
        logger.error("For more information, see the documentation.")
        raise RuntimeError("Completions only supported for bash.")

    if mode == "perm":
        if not shutil.which("uv"):
            logger.error(
                "'uv' command not found, which is required for permanent completion setup."
            )
            logger.error("Please install uv: https://github.com/astral-sh/uv")
            logger.error("For more information, see the documentation.")
            raise RuntimeError("'uv' command not found.")

        bashrc_path = Path.home() / ".bashrc"
        if not bashrc_path.is_file():
            logger.warning(f"~/.bashrc not found. Cannot set up permanent completions.")
            return

        completion_line = '# agro cli completions\neval "$(uvx --from argcomplete register-python-argcomplete agro)"\n'

        content = bashrc_path.read_text()
        if completion_line.strip() in content:
            logger.info("Agro completions already configured in ~/.bashrc.")
            return

        logger.info("Adding completions to ~/.bashrc...")
        with bashrc_path.open("a") as f:
            f.write("\n" + completion_line)
        logger.info(
            "✅ Permanent completions set up. Please restart your shell or run 'source ~/.bashrc'."
        )

    elif mode == "current":
        logger.info("To enable tab completion for the current session, run:")
        cmd = 'eval "$(register-python-argcomplete agro)"'
        logger.info(f"  {cmd}")
        if not shutil.which("register-python-argcomplete"):
            logger.warning(
                "\nWarning: 'register-python-argcomplete' not found in PATH."
            )
            logger.warning(
                "You may need to run: 'eval \"$(uvx --from argcomplete register-python-argcomplete agro)\"' instead."
            )


def create_task_file(task_name=None, show_cmd_output=False):
    """Creates a new task spec file and opens it in the editor."""
    if not task_name:
        try:
            task_name = input("Enter the task name: ")
        except (EOFError, KeyboardInterrupt):
            logger.warning("\nOperation cancelled.")
            return
        if not task_name:
            logger.warning("Task name cannot be empty. Operation cancelled.")
            return

    if task_name.endswith(".md"):
        logger.warning(
            "Task name should not include the .md extension. It will be added automatically."
        )
        task_name = task_name[:-3]

    specs_dir = Path(config.AGDOCS_DIR) / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)

    task_file_path = specs_dir / f"{task_name}.md"

    if not task_file_path.exists():
        logger.info(f"Creating new task file: {task_file_path}")
        task_file_path.touch()
    else:
        logger.info(f"Task file already exists: {task_file_path}")

    editor_cmd = config.AGRO_EDITOR_CMD
    if not editor_cmd:
        logger.warning("AGRO_EDITOR_CMD is not set in your config. Cannot open file.")
        logger.info(f"You can edit the file at: {task_file_path}")
        return

    logger.info(f"Opening {task_file_path} with '{editor_cmd}'...")

    command = shlex.split(editor_cmd) + [str(task_file_path)]

    try:
        subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        logger.error(
            f"Error: Command '{command[0]}' not found. Is it in your PATH?"
        )
        logger.info(f"You can edit the file at: {task_file_path}")
    except Exception as e:
        logger.error(f"Error opening editor: {e}")
        logger.info(f"You can edit the file at: {task_file_path}")


def _run_command(
    command,
    cwd=None,
    check=True,
    capture_output=False,
    shell=False,
    show_cmd_output=False,
    suppress_error_logging=False,
    timeout=None,
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
            timeout=timeout,
        )
        return result
    except subprocess.TimeoutExpired as e:
        if not suppress_error_logging:
            cmd_str = command if isinstance(command, str) else shlex.join(command)
            logger.error(f"Timeout of {timeout}s expired for command: {cmd_str}")
            # If output was captured, it's in the exception.
            if e.stdout:
                logger.error(f"STDOUT:\n{e.stdout.strip()}")
            if e.stderr:
                logger.error(f"STDERR:\n{e.stderr.strip()}")
        raise
    except subprocess.CalledProcessError as e:
        if not suppress_error_logging:
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


def _setup_python_environment(worktree_path, show_cmd_output):
    """Sets up the Python environment in the given worktree path."""
    logger.debug(f"Trying to set up Python environment in {worktree_path}...")

    has_pyproject = (worktree_path / "pyproject.toml").is_file()
    req_files = sorted(list(worktree_path.glob("requirements*.txt")))

    if not has_pyproject and not req_files:
        logger.warning(
            f"No pyproject.toml or requirements*.txt found in {worktree_path}. Skipping Python environment setup."
        )
        # current behavior: don't initialize uv isolated environment;
        # might change later
        return

    for cmd_str in config.ENV_SETUP_CMDS:
        command = shlex.split(cmd_str)
        if not command:
            continue
        _run_command(
            command,
            cwd=str(worktree_path),
            capture_output=True,
            show_cmd_output=show_cmd_output,
        )


def make_new_tree(index, fresh_env, no_overrides, show_cmd_output=False):
    """Creates a new git worktree with a dedicated environment."""
    tree_name = f"t{index}"
    branch_name = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
    worktree_path = Path(config.WORKTREE_DIR) / tree_name
    api_port = config.BASE_API_PORT + index

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

    agswap_dir = worktree_path / ".agswap"
    agswap_dir.mkdir()
    (agswap_dir / ".gitignore").write_text("*\n")
    logger.debug(f"Created worktree-specific swap dir: {agswap_dir}")

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

    _setup_python_environment(worktree_path, show_cmd_output)

    logger.debug("\n" + "🌴 New worktree created successfully.")
    logger.debug(f"   Worktree: {worktree_path}")
    logger.debug(f"   Branch: {branch_name}")
    if not no_overrides and env_file_created:
        logger.debug(f"   API Port: {api_port}")

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
            logger.debug(
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
            logger.debug(f"Branch '{branch_name}' not found. Skipping deletion.")

        logger.info(f"♻️  Cleanup for index {i} complete.")


def exec_agent(
    task_file,
    fresh_env,
    no_overrides,
    agent_args,
    exec_cmd=None,
    indices_str=None,
    num_trees=None,
    show_cmd_output=False,
    agent_type=None,
    auto_commit=True,
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
            index, fresh_env, no_overrides, show_cmd_output
        )

        worktree_path = Path(config.WORKTREE_DIR) / f"t{index}"
        agswap_dir = worktree_path / ".agswap"

        guides_src_dir = Path(config.AGDOCS_DIR) / "guides"
        guide_files_in_swap = []
        if guides_src_dir.is_dir():
            guides_dest_dir = agswap_dir / "guides"
            guides_dest_dir.mkdir(exist_ok=True)
            for guide_file in guides_src_dir.glob("*.md"):
                dest_file = guides_dest_dir / guide_file.name
                shutil.copy(guide_file, dest_file)
                guide_files_in_swap.append(dest_file)
            if guide_files_in_swap:
                logger.debug(
                    f"Copied {len(guide_files_in_swap)} guide files to {guides_dest_dir}"
                )

        task_in_swap_path = agswap_dir / task_path.name
        shutil.copy(task_path, task_in_swap_path)
        logger.debug(f"Copied task file to {task_in_swap_path}")

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

        pid_dir = Path(config.AGDOCS_DIR) / "swap"
        pid_dir.mkdir(parents=True, exist_ok=True)
        pid_file = pid_dir / f"t{index}.pid"

        logger.debug(f"Launching agent in detached mode from within {worktree_path}...")

        log_file_path = agswap_dir / "agro-exec.log"
        exec_command = exec_cmd or config.EXEC_CMD_DEFAULT

        agent_type_to_use = agent_type or config.AGENT_TYPE
        agent_config_data = config.AGENT_CONFIG.get(agent_type_to_use)
        if not agent_config_data:
            raise ValueError(f"Unknown or unsupported agent type: '{agent_type_to_use}'")

        command = [exec_command]
        command.extend(agent_config_data.get("args", []))

        if agent_type_to_use == "aider" and guide_files_in_swap:
            for guide_file in guide_files_in_swap:
                rel_path = guide_file.relative_to(worktree_path)
                command.extend(["--read", str(rel_path)])
            logger.debug(
                f"Added {len(guide_files_in_swap)} guide files with --read for aider."
            )

        if agent_type_to_use == "gemini":
            gemini_dir = worktree_path / ".gemini"
            if gemini_dir.exists():
                logger.warning(
                    f"Directory '{gemini_dir}' already exists. Gemini agent will not have access to guide files."
                )
            else:
                logger.debug(f"Creating '{gemini_dir}' for gemini agent context.")
                gemini_dir.mkdir()
                (gemini_dir / ".gitignore").write_text("*\n")
                if guide_files_in_swap:
                    relative_guide_paths = [
                        str(p.relative_to(worktree_path)) for p in guide_files_in_swap
                    ]
                    settings_content = {"contextFileName": relative_guide_paths}
                    settings_file = gemini_dir / "settings.json"
                    settings_file.write_text(json.dumps(settings_content, indent=4))
                    logger.debug(
                        f"Created '{settings_file}' with {len(relative_guide_paths)} guide files."
                    )

        task_file_rel_path = str(task_in_swap_path.relative_to(worktree_path))
        task_file_arg_template = agent_config_data.get("task_file_arg_template")

        if task_file_arg_template:
            task_args = [
                arg.format(task_file=task_file_rel_path)
                for arg in task_file_arg_template
            ]
            command.extend(task_args)

        command.extend(agent_args)

        popen_kwargs = {
            "cwd": str(worktree_path),
            "stderr": subprocess.STDOUT,
            "start_new_session": True,  # Detach from parent
        }

        # Apply timeout wrapper
        timeout_seconds = config.AGENT_TIMEOUTS.get(agent_type_to_use)
        if timeout_seconds:
            timeout_command = ["timeout", str(timeout_seconds)] + command
            command = timeout_command
            logger.debug(
                f"Applied timeout of {timeout_seconds} seconds to {agent_type_to_use} command"
            )

        with open(log_file_path, "wb") as log_file:
            popen_kwargs["stdout"] = log_file
            logger.debug(f"Running agents process: {str(command)}, {str(popen_kwargs.copy())}")
            if task_file_arg_template:
                # Agent takes task file as command-line argument
                process = subprocess.Popen(command, **popen_kwargs)
            else:
                # Agent takes task file via stdin
                with open(task_in_swap_path, "r") as task_f:
                    task_content = task_f.read()

                if agent_type_to_use == "claude" and guide_files_in_swap:
                    guides_ref = "@.agswap/guides/* "
                    task_content = guides_ref + task_content
                    logger.debug(
                        "Prepended claude guide file reference to task content."
                    )

                popen_kwargs["stdin"] = subprocess.PIPE
                process = subprocess.Popen(command, **popen_kwargs)
                if process.stdin:
                    process.stdin.write(task_content.encode("utf-8"))
                    process.stdin.close()

        pid_file.write_text(str(process.pid))

        if auto_commit and agent_type_to_use != "aider":
            logger.debug(f"Spawning auto-commit monitor for worktree {worktree_path}")
            committer_cmd = [
                sys.executable,
                "-m",
                "agro.committer",
                str(process.pid),
                str(worktree_path.resolve()),
                task_path.name,
                agent_type_to_use,
            ]
            committer_process = subprocess.Popen(committer_cmd)
            logger.debug(f"Committer PID: {committer_process.pid}")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"🏃 Agent for index {index} started successfully.")
        logger.info(f"   Worktree: {worktree_path.resolve()}")
        logger.info(f"   Task file: {task_path.resolve()}")
        logger.info(f"   Branch: {new_branch_name}")
        logger.info(f"   Agent type: {agent_type_to_use}")
        logger.info(f"   Initial commit SHA: {initial_sha[:6]}")
        logger.info(f"   Start time: {current_time}")
        logger.debug(f"   PID: {process.pid} (saved to {pid_file.resolve()})")
        logger.debug(f"   Log file: {log_file_path.resolve()}")
        logger.debug(f"   Task file copy: {task_in_swap_path.resolve()}")


def _get_indices_from_branch_patterns(branch_patterns=None, show_cmd_output=False) -> list[int]:
    """
    Resolves branch patterns to a list of worktree indices.
    If no patterns are provided, returns indices for all existing worktrees.
    """
    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
    if not worktree_state:
        return []

    if not branch_patterns:
        # Return all indices if no pattern is given
        all_indices = []
        for wt_name in worktree_state.keys():
            if wt_name.startswith("t") and wt_name[1:].isdigit():
                all_indices.append(int(wt_name[1:]))
        return sorted(all_indices)

    all_matching_branches = set()
    for pattern in branch_patterns:
        matching_branches = _get_matching_branches(
            pattern, show_cmd_output=show_cmd_output
        )
        all_matching_branches.update(matching_branches)

    if not all_matching_branches:
        patterns_str = " ".join(f"'{p}'" for p in branch_patterns)
        logger.info(f"No branches found matching patterns: {patterns_str}")
        return []

    matching_indices = []
    for wt_name, branch in worktree_state.items():
        if branch in all_matching_branches:
            if wt_name.startswith("t") and wt_name[1:].isdigit():
                matching_indices.append(int(wt_name[1:]))

    return sorted(matching_indices)


def diff_worktrees(branch_patterns, diff_opts=None, show_cmd_output=False):
    """Runs 'git diff' in multiple worktrees."""
    # Default to output branches if no pattern is provided
    if not branch_patterns:
        patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
        logger.info(
            f"No branch pattern specified. Using default pattern for output branches: '{config.WORKTREE_OUTPUT_BRANCH_PREFIX}*'"
        )
    else:
        patterns_to_use = branch_patterns

    indices = _get_indices_from_branch_patterns(patterns_to_use, show_cmd_output)
    if not indices:
        logger.warning("No worktrees found matching the provided patterns.")
        return

    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)

    for index in indices:
        tree_name = f"t{index}"
        worktree_path = Path(config.WORKTREE_DIR) / tree_name
        branch_name = worktree_state.get(tree_name, "<unknown branch>")

        if not worktree_path.is_dir():
            logger.warning(
                f"Worktree t{index} at '{worktree_path}' not found. Skipping."
            )
            continue

        logger.info(f"\n--- Diff for t{index} ({branch_name}) ---")

        original_branch = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
        command = ["git", "diff"]

        pre_opts = []
        pathspec = []
        if diff_opts:
            if "--" in diff_opts:
                dd_idx = diff_opts.index("--")
                pre_opts = diff_opts[:dd_idx]
                pathspec = diff_opts[dd_idx + 1 :]
            else:
                pre_opts = diff_opts

        if pathspec:
            # When a pathspec is provided, add options, then commits, then '--' and paths
            command.extend(pre_opts)
            command.extend([original_branch, "HEAD"])
            command.append("--")
            command.extend(pathspec)
        else:
            # No pathspec: place options before the commits
            command.extend(pre_opts)
            command.extend([original_branch, "HEAD"])

        cmd_str = shlex.join(command)
        logger.info(f"$ {cmd_str}")

        try:
            _run_command(
                command,
                cwd=str(worktree_path),
                show_cmd_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # _run_command already prints details.
            logger.error(f"--- Command failed in t{index}. Continuing... ---")
            continue


def muster_command(
    command_str,
    branch_patterns,
    show_cmd_output=False,
    common_cmd_key=None,
    timeout=None,
):
    """Runs a command in multiple worktrees."""
    final_command_str = None
    cmd_timeout = None

    if common_cmd_key:
        common_cmd_config = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
        if not common_cmd_config:
            config_path = Path(config.AGDOCS_DIR) / "conf" / "agro.conf.yml"
            msg = f"Common command '{common_cmd_key}' not found in 'MUSTER_COMMON_CMDS'."
            if config_path.is_file():
                msg += f" Check your config file at '{config_path}'."
            else:
                msg += f" No config file found at '{config_path}'."

            available_cmds = ", ".join(sorted(config.MUSTER_COMMON_CMDS.keys()))
            if available_cmds:
                msg += f" Available commands are: {available_cmds}."
            raise ValueError(msg)

        if isinstance(common_cmd_config, dict):
            final_command_str = common_cmd_config.get("cmd")
            if "timeout" in common_cmd_config:
                cmd_timeout = common_cmd_config.get("timeout")
                if cmd_timeout is None:
                    cmd_timeout = 0
        else:  # Support old string-only format
            final_command_str = common_cmd_config

        if not final_command_str:
            raise ValueError(f"Command not found for common command key '{common_cmd_key}'")
    else:
        final_command_str = command_str

    # Determine timeout: CLI > common_cmd config > global config > default
    if timeout is not None:
        effective_timeout = timeout if timeout > 0 else None
    elif cmd_timeout is not None:
        effective_timeout = cmd_timeout if cmd_timeout > 0 else None
    else:
        effective_timeout = (
            config.MUSTER_DEFAULT_TIMEOUT if config.MUSTER_DEFAULT_TIMEOUT > 0 else None
        )

    if not branch_patterns:
        patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
        logger.info(
            f"No branch pattern specified. Using default pattern for output branches: '{config.WORKTREE_OUTPUT_BRANCH_PREFIX}*'"
        )
    else:
        patterns_to_use = branch_patterns

    indices = _get_indices_from_branch_patterns(patterns_to_use, show_cmd_output)
    if not indices:
        logger.warning("No worktrees found matching the provided patterns.")
        return

    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)

    if not final_command_str:
        raise ValueError("Empty command provided.")

    # Detect if shell is needed for complex commands (e.g., with pipes, redirects)
    shell_chars = ['|', '&', ';', '<', '>', '(', ')', '$', '`']
    use_shell = any(char in final_command_str for char in shell_chars)

    if use_shell:
        command = final_command_str
    else:
        command = shlex.split(final_command_str)
        if not command:
            raise ValueError("Empty command provided.")

    for index in indices:
        tree_name = f"t{index}"
        worktree_path = Path(config.WORKTREE_DIR) / tree_name
        branch_name = worktree_state.get(tree_name, "<unknown branch>")

        if not worktree_path.is_dir():
            logger.warning(
                f"Worktree t{index} at '{worktree_path}' not found. Skipping."
            )
            continue

        logger.info(f"\n--- Running command in t{index} ({branch_name}) ---")
        logger.info(f"$ {final_command_str}")
        try:
            _run_command(
                command,
                cwd=str(worktree_path),
                shell=use_shell,
                show_cmd_output=True,
                timeout=effective_timeout,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
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
            suppress_error_logging=True,
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
            # Re-raise if it's a different error, but log it first
            cmd_str = shlex.join(["git", "checkout", branch_name])
            logger.error(f"Error executing command: {cmd_str}")
            if e.stdout:
                logger.error(f"STDOUT:\n{e.stdout.strip()}")
            if e.stderr:
                logger.error(f"STDERR:\n{e.stderr.strip()}")
            raise


def fade_branches(patterns, show_cmd_output=False):
    """Deletes local git branches matching patterns after user confirmation."""
    patterns_str = " ".join(f"'{p}'" for p in patterns)
    logger.info(f"Searching for branches matching patterns: {patterns_str}")

    all_matching_branches = set()
    for pattern in patterns:
        matching_branches = _get_matching_branches(
            pattern, show_cmd_output=show_cmd_output
        )
        all_matching_branches.update(matching_branches)

    if not all_matching_branches:
        logger.info("No branches found matching the patterns to delete.")
        return

    result = _run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        check=True,
        show_cmd_output=show_cmd_output,
    )
    current_branch = result.stdout.strip()

    branches_to_delete = []
    for branch_name in sorted(list(all_matching_branches)):
        if branch_name == current_branch:
            logger.warning(f"Skipping currently checked out branch '{branch_name}'")
            continue
        branches_to_delete.append(branch_name)

    if not branches_to_delete:
        logger.info("No branches to delete after filtering out the current branch.")
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


def clean_worktrees(branch_patterns=None, mode="hard", show_cmd_output=False):
    """Deletes worktrees and optionally their branches based on patterns."""
    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
    if not worktree_state and not branch_patterns:
        logger.info("No worktrees found to clean.")
        return

    if not branch_patterns:
        patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
        logger.info(
            f"No branch pattern specified. Using default pattern for output branches: '{config.WORKTREE_OUTPUT_BRANCH_PREFIX}*'"
        )
    else:
        patterns_to_use = branch_patterns

    all_matching_branches = set()
    for pattern in patterns_to_use:
        matching_branches = _get_matching_branches(
            pattern, show_cmd_output=show_cmd_output
        )
        all_matching_branches.update(matching_branches)

    worktrees_to_delete = {}  # 't1': 'output/branch.1'
    for wt_name, branch in worktree_state.items():
        if branch in all_matching_branches:
            worktrees_to_delete[wt_name] = branch

    branches_to_delete = all_matching_branches if mode == "hard" else set()

    if not worktrees_to_delete and not branches_to_delete:
        logger.info("No worktrees or branches found matching the criteria to clean.")
        return

    logger.info("\n--- Dry Run ---")
    if worktrees_to_delete:
        logger.info("The following worktrees will be deleted:")
        for wt_name, branch in sorted(worktrees_to_delete.items()):
            logger.info(f"  - {wt_name} (branch: {branch})")

    if branches_to_delete:
        logger.info("The following branches will be deleted (hard clean):")
        for branch in sorted(list(branches_to_delete)):
            logger.info(f"  - {branch}")
    logger.info("--- End Dry Run ---\n")

    try:
        confirm = input("Proceed with cleaning? [Y/n]: ")
    except (EOFError, KeyboardInterrupt):
        logger.warning("\nOperation cancelled.")
        return
    if confirm.lower() not in ("y", ""):
        logger.warning("Operation cancelled by user.")
        return

    if worktrees_to_delete:
        indices_to_delete = [int(wt_name[1:]) for wt_name in worktrees_to_delete]
        logger.info("\nDeleting worktrees...")
        for index in sorted(indices_to_delete):
            try:
                # This will not trigger confirmation prompt in delete_tree
                delete_tree(str(index), show_cmd_output=show_cmd_output)
            except Exception as e:
                logger.error(f"Failed to delete worktree for index {index}: {e}")

    if branches_to_delete:
        logger.info("\nDeleting branches (hard clean)...")
        result = _run_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            check=True,
            show_cmd_output=show_cmd_output,
        )
        current_branch = result.stdout.strip()

        deleted_count = 0
        failed_count = 0
        for branch in sorted(list(branches_to_delete)):
            if branch == current_branch:
                logger.warning(f"Skipping currently checked out branch '{branch}'")
                continue

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
            f"\nBranch cleanup complete. Deleted {deleted_count} branches, {failed_count} failed."
        )

    logger.info("\n✅ Clean complete.")


def mirror_docs(show_cmd_output=False):
    """Mirrors the documentation directory to its public counterpart."""
    source_dir_str = config.AGDOCS_DIR
    dest_dir_str = config.PUBLIC_AGDOCS_DIR

    source_dir = Path(source_dir_str)
    dest_dir = Path(dest_dir_str)

    if not source_dir.is_dir():
        logger.error(f"Source directory '{source_dir}' not found.")
        raise FileNotFoundError(f"Source directory '{source_dir}' not found.")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Ensure source and dest paths have a trailing slash for rsync
    source_path = source_dir_str if source_dir_str.endswith('/') else f"{source_dir_str}/"
    dest_path = dest_dir_str if dest_dir_str.endswith('/') else f"{dest_dir_str}/"

    command = ["rsync", "-av", "--delete", source_path, dest_path]

    logger.info(f"Mirroring '{source_path}' to '{dest_path}'...")
    _run_command(command, show_cmd_output=show_cmd_output)
    logger.info("✅ Mirroring complete.")


def get_worktree_state(show_cmd_output=False):
    """
    Retrieves the state of all worktrees, mapping worktree name to its current branch.
    """
    worktree_dir = Path(config.WORKTREE_DIR)
    if not worktree_dir.is_dir():
        return {}

    state = {}
    worktree_paths = sorted(
        [p for p in worktree_dir.iterdir() if p.is_dir() and p.name.startswith("t")]
    )
    for worktree_path in worktree_paths:
        try:
            result = _run_command(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=worktree_path,
                capture_output=True,
                check=True,
                show_cmd_output=show_cmd_output,
                suppress_error_logging=True,
            )
            branch = result.stdout.strip()
            state[worktree_path.name] = branch
        except subprocess.CalledProcessError:
            state[worktree_path.name] = "<error: unable to get branch>"
        except FileNotFoundError:
            state[worktree_path.name] = "<error: git not found>"
    return state


def state(branch_patterns=None, show_cmd_output=False):
    """Prints the state of the worktrees, optionally filtered by branch pattern."""
    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)

    if branch_patterns:
        all_matching_branches = set()
        for pattern in branch_patterns:
            matching_branches = _get_matching_branches(
                pattern, show_cmd_output=show_cmd_output
            )
            all_matching_branches.update(matching_branches)

        if not all_matching_branches:
            patterns_str = " ".join(f"'{p}'" for p in branch_patterns)
            logger.info(f"No branches found matching patterns: {patterns_str}")
            return

        worktree_state = {
            wt: br
            for wt, br in worktree_state.items()
            if br in all_matching_branches
        }

    if not worktree_state:
        logger.info("No worktrees found matching the criteria.")
        return

    for worktree, branch in sorted(worktree_state.items()):
        logger.info(f"{worktree}: {branch}")


def surrender(branch_patterns=None, show_cmd_output=False):
    """Kills running agent processes associated with worktrees."""
    pid_dir = Path(config.AGDOCS_DIR) / "swap"
    if not pid_dir.is_dir():
        logger.info("No agent processes seem to be running (PID directory not found).")
        return

    target_indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
    if not target_indices:
        if branch_patterns:
            logger.warning("No worktrees found matching the provided patterns.")
        else:
            logger.info("No worktrees found.")
        return

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
