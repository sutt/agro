import argparse
import sys

from . import core


def main():
    """
    Main entry point for the agscript command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="A script to manage git worktrees for agent-based development.",
        prog="agscript",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
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

    # --- make command ---
    parser_make = subparsers.add_parser(
        "make",
        parents=[common_parser],
        help="Create a new worktree.",
    )
    parser_make.add_argument("index", type=int, help="Index for the new worktree.")
    parser_make.set_defaults(
        func=lambda args: core.make_new_tree(
            args.index, args.fresh_env, args.no_env_overrides
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
            args.taskfile,
            args.agent_args,
        )
    )

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
