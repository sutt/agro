import argparse
import os
import sys

from . import core


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
    remaining_args = args.agent_args

    indices_str = None
    agent_args = []

    if remaining_args and _is_indices_list(remaining_args[0]):
        indices_str = remaining_args[0]
        agent_args = remaining_args[1:]
    else:
        agent_args = remaining_args

    core.exec_agent(
        taskfile,
        indices_str,
        args.fresh_env,
        args.no_env_overrides,
        args.no_all_extras,
        agent_args,
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
  exec <taskfile> [indices]     Run an agent in new worktree(s).
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
            args.index, args.fresh_env, args.no_env_overrides, args.no_all_extras
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
        func=lambda args: core.delete_tree(indices_str=args.indices, all_flag=args.all)
    )

    # --- exec command ---
    parser_exec = subparsers.add_parser(
        "exec",
        parents=[common_parser],
        help="Re-creates worktree(s) and executes detached agent processes. "
        "All arguments after the taskfile and optional indices are passed to the agent.",
    )
    parser_exec.add_argument(
        "taskfile", help="The taskfile for the agent (e.g., tasks/my-task.md)."
    )
    parser_exec.add_argument(
        "agent_args",
        nargs=argparse.REMAINDER,
        help="Optional indices (e.g. '1,2') followed by arguments for maider.sh.",
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
            args.command_str, args.indices, server=args.server, kill_server=args.kill_server
        )
    )

    # --- grab command ---
    parser_grab = subparsers.add_parser(
        "grab", help="Checkout a branch, creating a copy if it's in use by another worktree."
    )
    parser_grab.add_argument("branch_name", help="The branch to grab.")
    parser_grab.set_defaults(func=lambda args: core.grab_branch(args.branch_name))

    # --- fade command ---
    parser_fade = subparsers.add_parser(
        "fade", help="Delete local branches matching a regex pattern after confirmation."
    )
    parser_fade.add_argument("pattern", help="The regex pattern to match branch names against.")
    parser_fade.set_defaults(func=lambda args: core.fade_branches(args.pattern))

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
    parser_surrender.set_defaults(func=lambda args: core.surrender(args.indices))

    # --- help command ---
    parser_help = subparsers.add_parser("help", help="Show this help message.")
    parser_help.set_defaults(func=lambda args: parser.print_help())

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
