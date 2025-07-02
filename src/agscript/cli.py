import argparse
import os
import sys

from . import core


def main():
    """
    Main entry point for the agscript command-line interface.
    """
    swap_dir = ".agdocs/swap"
    os.makedirs(swap_dir, exist_ok=True)
    gitignore_path = os.path.join(swap_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write("*\n")

    epilog_text = """Available commands:
  make <index>                  Create a new worktree.
  delete <index>                Delete the worktree with the given index.
  exec <index> <taskfile> ...   Run an agent in a new worktree.
  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <pattern>                Delete local branches matching a regex pattern.
  surrender [indices]           Kill running agent processes (default: all).
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
        prog="agscript",
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
    parser_delete = subparsers.add_parser(
        "delete", help="Delete the worktree with the given index."
    )
    parser_delete.add_argument(
        "index", type=int, help="Index of the worktree to delete."
    )
    parser_delete.set_defaults(func=lambda args: core.delete_tree(args.index))

    # --- exec command ---
    parser_exec = subparsers.add_parser(
        "exec",
        parents=[common_parser],
        help="Re-creates a worktree and executes a detached agent process. "
        "All arguments after the taskfile are passed to the agent.",
    )
    parser_exec.add_argument("index", type=int, help="Index for the worktree.")
    parser_exec.add_argument(
        "taskfile", help="The taskfile for the agent (e.g., tasks/my-task.md)."
    )
    parser_exec.add_argument(
        "agent_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to the maider.sh script.",
    )
    parser_exec.set_defaults(
        func=lambda args: core.exec_agent(
            args.index,
            args.fresh_env,
            args.no_env_overrides,
            args.no_all_extras,
            args.taskfile,
            args.agent_args,
        )
    )

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
