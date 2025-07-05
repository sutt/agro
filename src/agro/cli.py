import argparse
import logging
import os
import sys

from . import core, __version__


def _is_indices_list(s):
    """Check if a string is a comma-separated list of digits."""
    if not s:
        return False
    parts = s.split(',')
    if not any(p.strip() for p in parts):  # handles ',' or ',,'
        return False
    return all(p.strip().isdigit() for p in parts if p.strip())


def _dispatch_exec(args):
    """Helper to dispatch exec command with complex argument parsing."""
    taskfile = args.taskfile
    agent_args = args.agent_args

    num_trees = args.num_trees_pos or args.num_trees_opt

    core.exec_agent(
        task_file=taskfile,
        fresh_env=args.fresh_env,
        no_overrides=args.no_env_overrides,
        no_all_extras=args.no_all_extras,
        agent_args=agent_args,
        indices_str=args.tree_indices,
        num_trees=num_trees,
        show_cmd_output=(args.verbose >= 2),
    )


def main():
    """
    Main entry point for the agro command-line interface.
    """
    swap_dir = ".agdocs/swap"
    os.makedirs(swap_dir, exist_ok=True)
    gitignore_path = os.path.join(swap_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write("*\n")

    epilog_text = """Available commands:
  exec <taskfile> [num-trees]   Run an agent in new worktree(s), see also -n and -t.
  surrender [indices]           Kill running agent processes (default: all).
  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <pattern>                Delete local branches matching a regex pattern.
  make <index>                  Create a new worktree.
  delete <indices>|--all        Delete one, multiple, or all worktrees.
  help                          Show this help message.

Common options for 'make' and 'exec':
  --fresh-env         When creating a worktree, use .env.example as the base instead of .env.
  --no-env-overrides  When creating a worktree, do not add port overrides to the .env file.
  --no-all-extras     Do not install all extra dependencies when running 'uv sync'.

Options for 'muster':
  -s, --server        Run command as a background server, redirecting output and saving PID.
  -k, --kill-server   Kill the background server and clean up pid/log files."""

    parser = argparse.ArgumentParser(
        description="A script to manage git worktrees for agent-based development.",
        prog="agro",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity. -v for debug, -vv for command output.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output except warnings and errors.",
    )
    subparsers = parser.add_subparsers(dest="command", help=argparse.SUPPRESS)
    subparsers.required = True

    # --- Common arguments for make and exec ---
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--fresh-env",
        action="store_true",
        help="When creating a worktree, use .env.example as the base instead of .env.",
    )
    common_parser.add_argument(
        "--no-env-overrides",
        action="store_true",
        help="When creating a worktree, do not add port overrides to the .env file.",
    )
    common_parser.add_argument(
        "--no-all-extras",
        action="store_true",
        help="Do not install all extra dependencies when running 'uv sync'.",
    )

    # --- make command ---
    parser_make = subparsers.add_parser(
        "make",
        parents=[common_parser],
        help="Create a new worktree.",
    )
    parser_make.add_argument("index", type=int, help="Index for the new worktree.")
    parser_make.set_defaults(
        func=lambda args: core.make_new_tree(
            args.index,
            args.fresh_env,
            args.no_env_overrides,
            args.no_all_extras,
            show_cmd_output=(args.verbose >= 2),
        )
    )

    # --- delete command ---
    parser_delete = subparsers.add_parser("delete", help="Delete one or all worktrees.")
    delete_group = parser_delete.add_mutually_exclusive_group(required=True)
    delete_group.add_argument(
        "indices",
        nargs="?",
        type=str,
        help="Comma-separated list of worktree indices to delete (e.g., '1,2').",
    )
    delete_group.add_argument(
        "--all", action="store_true", help="Delete all existing worktrees."
    )
    parser_delete.set_defaults(
        func=lambda args: core.delete_tree(
            indices_str=args.indices,
            all_flag=args.all,
            show_cmd_output=(args.verbose >= 2),
        )
    )

    # --- exec command ---
    parser_exec = subparsers.add_parser(
        "exec",
        parents=[common_parser],
        help="Re-creates worktree(s) and executes detached agent processes. "
        "All arguments after the taskfile and exec options are passed to the agent.",
    )
    parser_exec.add_argument(
        "taskfile", help="The taskfile for the agent (e.g., tasks/my-task.md)."
    )

    exec_group = parser_exec.add_mutually_exclusive_group()
    exec_group.add_argument(
        "num_trees_pos",
        nargs="?",
        type=int,
        default=None,
        metavar="num-trees",
        help="Number of new worktrees to create.",
    )
    exec_group.add_argument(
        "-n",
        "--num-trees",
        type=int,
        dest="num_trees_opt",
        help="Number of new worktrees to create.",
    )
    exec_group.add_argument(
        "-t",
        "--tree-indices",
        help="Comma-separated list of worktree indices to use (e.g., '1,2').",
    )

    parser_exec.add_argument(
        "agent_args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to cli-coder (Not Implemented)",
    )
    parser_exec.set_defaults(func=_dispatch_exec)

    # --- muster command ---
    parser_muster = subparsers.add_parser(
        "muster", help="Run a command in specified worktrees."
    )
    parser_muster.add_argument(
        "command_str",
        help="The command to execute. A dummy value can be used with --kill-server.",
    )
    parser_muster.add_argument(
        "indices", help="Comma-separated list of worktree indices (e.g., '1,2')."
    )
    parser_muster.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="Run command as a background server, redirecting output and saving PID.",
    )
    parser_muster.add_argument(
        "-k",
        "--kill-server",
        action="store_true",
        help="Kill the background server and clean up pid/log files.",
    )
    parser_muster.set_defaults(
        func=lambda args: core.muster_command(
            args.command_str,
            args.indices,
            server=args.server,
            kill_server=args.kill_server,
            show_cmd_output=(args.verbose >= 2),
        )
    )

    # --- grab command ---
    parser_grab = subparsers.add_parser(
        "grab", help="Checkout a branch, creating a copy if it's in use by another worktree."
    )
    parser_grab.add_argument("branch_name", help="The branch to grab.")
    parser_grab.set_defaults(
        func=lambda args: core.grab_branch(
            args.branch_name, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- fade command ---
    parser_fade = subparsers.add_parser(
        "fade", help="Delete local branches matching a regex pattern after confirmation."
    )
    parser_fade.add_argument("pattern", help="The regex pattern to match branch names against.")
    parser_fade.set_defaults(
        func=lambda args: core.fade_branches(
            args.pattern, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- surrender command ---
    parser_surrender = subparsers.add_parser(
        "surrender", help="Kill running agent processes."
    )
    parser_surrender.add_argument(
        "indices",
        nargs="?",
        default="all",
        help="Comma-separated list of worktree indices (e.g., '1,2'). Defaults to all.",
    )
    parser_surrender.set_defaults(
        func=lambda args: core.surrender(
            args.indices, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- help command ---
    parser_help = subparsers.add_parser("help", help="Show this help message.")
    parser_help.set_defaults(func=lambda args: parser.print_help())

    try:
        args = parser.parse_args()

        # Setup logging
        if args.quiet:
            log_level = logging.WARNING
        elif args.verbose >= 1:
            log_level = logging.DEBUG
        else:  # verbose == 0
            log_level = logging.INFO

        logger = logging.getLogger("agro")
        logger.setLevel(log_level)

        # Handler for stdout (INFO, DEBUG)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(stdout_handler)

        # Handler for stderr (WARNING, ERROR, CRITICAL)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(stderr_handler)

        logger.propagate = False

        args.func(args)
    except Exception as e:
        logging.getLogger("agro").error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
