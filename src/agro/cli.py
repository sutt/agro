import argcomplete
import argparse
import logging
import os
import sys

from . import core, __version__


logger = logging.getLogger("agro")


def branch_completer(prefix, parsed_args, **kwargs):
    """A completer for git branch names."""
    try:
        all_branches = core._get_all_branches()
    except Exception:
        return []

    if not prefix:
        # Default to output branches if no prefix
        default_prefix = core.config.WORKTREE_OUTPUT_BRANCH_PREFIX
        return [b for b in all_branches if b.startswith(default_prefix)]

    return [b for b in all_branches if b.startswith(prefix)]


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
    agent_args = args.agent_args.copy()

    num_trees = args.num_trees_opt
    exec_cmd = args.exec_cmd_opt
    taskfile = None

    # Extract non-dashed arguments from the beginning of agent_args
    pos_args = []
    while agent_args and not agent_args[0].startswith("-"):
        pos_args.append(agent_args.pop(0))

    # First pass: find num_trees
    remaining_pos_args = []
    for arg in pos_args:
        if arg.isdigit():
            if num_trees is not None:
                raise ValueError(
                    "Number of trees specified twice (e.g. positionally and with -n)."
                )
            num_trees = int(arg)
        else:
            remaining_pos_args.append(arg)

    # Second pass: find taskfile from remaining string args
    unmatched_args = []
    for arg in remaining_pos_args:
        found_path = core.find_task_file(arg)
        if found_path and taskfile is None:
            taskfile = str(found_path)
        else:
            unmatched_args.append(arg)

    # Third pass: find exec_cmd from remaining args
    for arg in unmatched_args:
        if exec_cmd is not None:
            raise ValueError("Cannot specify exec-cmd twice.")
        exec_cmd = arg

    if not taskfile:
        # find most recent
        found_path = core.find_most_recent_task_file()
        if found_path:
            logger.info(f"No task file specified. Using most recent: {found_path}")
            try:
                confirm = input("Proceed with this task file? [Y/n]: ")
                if confirm.lower() not in ("y", ""):
                    logger.info("Operation cancelled.")
                    return
            except (EOFError, KeyboardInterrupt):
                logger.warning("\nOperation cancelled.")
                return
            taskfile = str(found_path)
        else:
            raise FileNotFoundError(
                "No task file specified and no task files found in default directory."
            )

    agent_type = args.agent_type_opt

    # Infer agent_type from exec_cmd if not provided
    if exec_cmd and not agent_type:
        for at in core.config.AGENT_CONFIG:
            if at in exec_cmd:
                agent_type = at
                logger.debug(f"Inferred agent type '{agent_type}' from exec_cmd '{exec_cmd}'")
                break
    # Infer exec_cmd from agent_type if not provided
    elif agent_type and not exec_cmd:
        exec_cmd = agent_type
        logger.debug(f"Inferred exec_cmd '{exec_cmd}' from agent_type '{agent_type}'")

    core.exec_agent(
        task_file=taskfile,
        fresh_env=args.fresh_env,
        no_overrides=args.no_env_overrides,
        agent_args=agent_args,
        exec_cmd=exec_cmd,
        indices_str=None,
        num_trees=num_trees,
        show_cmd_output=(args.verbose >= 2),
        agent_type=agent_type,
        auto_commit=not args.no_auto_commit,
    )


def _dispatch_init(args):
    """Helper to dispatch init command."""
    show_output = args.verbose >= 2
    # If --completions is used, only do that.
    if args.completions:
        core.setup_completions(mode=args.completions, show_cmd_output=show_output)
        return

    # Otherwise, do the normal init...
    core.init_project(conf_only=args.conf)

    # ...and if it's a full init (not --conf), also set up completions.
    if not args.conf:
        core.setup_completions(mode="current", show_cmd_output=show_output)


def _dispatch_muster(args):
    """Helper to dispatch muster command with complex argument parsing."""
    command_str = args.command_str
    branch_patterns = args.branch_patterns
    common_cmd_key = args.common_cmd_key

    if common_cmd_key:
        if command_str:
            # Positional command_str is treated as a branch pattern when -c is used
            branch_patterns.insert(0, command_str)
        command_str = None  # Command will be looked up from config
    elif not command_str:
        raise ValueError(
            "Muster command requires a command string or -c/--common-cmd option."
        )

    core.muster_command(
        command_str=command_str,
        branch_patterns=branch_patterns,
        common_cmd_key=common_cmd_key,
        show_cmd_output=(args.verbose >= 2),
        timeout=args.timeout,
    )


def _dispatch_diff(args):
    """Helper to dispatch diff command with complex argument parsing."""
    core.diff_worktrees(
        branch_patterns=args.branch_patterns,
        diff_opts=args.diff_opts,
        show_cmd_output=(args.verbose >= 2),
    )


def main():
    """
    Main entry point for the agro command-line interface.
    """
    epilog_text = """Main command:
  exec [args] [taskfile] [num-trees] [exec-cmd]   
                                
    Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees / agents to create.
          -c <exec-cmd>         Custom command to launch agent on worktree.
          -a <agent-type>       Specify agent type to override config.
                                Supported: aider, claude, gemini.

Other Commands:
  muster [opts] [command] [branch-patterns]    Run a command in specified worktrees.
  diff [branch-patterns] [diff-opts]   Show git diff for specified worktrees.
  surrender [branch-patterns]   Kill running agent processes (default: all).
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <branch-patterns>        Delete local branches matching a regex pattern.
  clean [opts] [branch-patterns]    Clean up worktrees and/or branches.
  state [branch-patterns]       Show the worktree to branch mappings (default: all).
  task [task-name]              Create a new task spec file and open it.
  init                          Initialize agro project structure in .agdocs/.
  mirror                        Mirror internal docs to public docs directory.
  make <index>                  Create a new worktree.
  delete <indices>|--all        Delete one, multiple, or all worktrees.

Branch-patterns examples (for regex like matching):
  output/add-thing              Match output/add-thing*
  output/add-thing.{2,5}        Match output/add-thing.2, output/add-thing.5
  output/add-thing.{1-4}        Match output/add-thing.1, ... output/add-thing.4

Common options for 'make' and 'exec':
  --fresh-env         Use .env.example as the base instead of .env.
  --no-env-overrides  Do not add port overrides to the .env file.

Options for 'muster':
  -c, --common-cmd <key> Run a pre-defined command from config.
  --timeout <seconds>   Override command timeout. 0 for no timeout.

Options for 'clean':
  --soft              Only delete worktrees, not branches.
  --hard              Delete both worktrees and branches (default).
    
Options for 'init':
  --conf              Only add a template agro.conf.yml to .agdocs/conf
  --completions [perm]  Setup shell completions ('perm' for permanent)."""
    parser = argparse.ArgumentParser(
        description="A script to manage git branches & worktrees for agent-based development.",
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

    # --- init command ---
    parser_init = subparsers.add_parser(
        "init",
        help="Initialize the .agdocs directory structure for the project.",
    )
    init_group = parser_init.add_mutually_exclusive_group()
    init_group.add_argument(
        "--conf",
        action="store_true",
        help="Only generate a blank config file. Fails if the file already exists.",
    )
    init_group.add_argument(
        "--completions",
        nargs="?",
        const="current",
        default=None,
        choices=["current", "perm"],
        help="Setup shell completions. With no argument, sets up for current session. Use 'perm' for permanent setup via .bashrc.",
    )
    parser_init.set_defaults(func=_dispatch_init)

    # --- mirror command ---
    parser_mirror = subparsers.add_parser(
        "mirror",
        help="Mirror the internal docs to the public docs directory.",
    )
    parser_mirror.set_defaults(
        func=lambda args: core.mirror_docs(show_cmd_output=(args.verbose >= 2))
    )

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
            args.index,
            args.fresh_env,
            args.no_env_overrides,
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
        "-n",
        "--num-trees",
        type=int,
        dest="num_trees_opt",
        help="Number of new worktrees to create.",
    )

    parser_exec.add_argument(
        "-c",
        "--exec-cmd",
        dest="exec_cmd_opt",
        help="Run the exec-cmd to launch agent on worktree.",
    )

    parser_exec.add_argument(
        "-a",
        "--agent-type",
        dest="agent_type_opt",
        help="Specify agent type to override config (e.g., 'aider', 'claude', 'gemini').",
    )

    parser_exec.add_argument(
        "--no-auto-commit",
        action="store_true",
        help="Disable automatic committing of changes after agent run.",
    )

    parser_exec.add_argument(
        "agent_args",
        nargs=argparse.REMAINDER,
        help="Optional [taskfile], [num-trees], [exec-cmd], and arguments to pass to the agent command.",
    )
    parser_exec.set_defaults(func=_dispatch_exec)

    # --- muster command ---
    parser_muster = subparsers.add_parser(
        "muster", help="Run a command in specified worktrees."
    )
    parser_muster.add_argument(
        "-c",
        "--common-cmd",
        dest="common_cmd_key",
        help="Run a pre-defined command from config.",
    )
    parser_muster.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Timeout in seconds for the command. Use 0 for no timeout.",
    )
    parser_muster.add_argument(
        "command_str",
        nargs="?",
        default=None,
        help="The command to execute. Optional if -c is used.",
    )
    parser_muster.add_argument(
        "branch_patterns",
        nargs="*",
        default=[],
        help="One or more branch patterns. Defaults to output branches.",
    ).completer = branch_completer
    parser_muster.set_defaults(func=_dispatch_muster)

    # --- diff command ---
    parser_diff = subparsers.add_parser(
        "diff", help="Show git diff for specified worktrees."
    )
    parser_diff.add_argument(
        "branch_patterns",
        nargs="*",
        default=[],
        help="Optional branch pattern(s).",
    ).completer = branch_completer
    parser_diff.set_defaults(func=_dispatch_diff)

    # --- grab command ---
    parser_grab = subparsers.add_parser(
        "grab", help="Checkout a branch, creating a copy if it's in use by another worktree."
    )
    parser_grab.add_argument("branch_name", help="The branch to grab.").completer = branch_completer
    parser_grab.set_defaults(
        func=lambda args: core.grab_branch(
            args.branch_name, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- fade command ---
    parser_fade = subparsers.add_parser(
        "fade", help="Delete local branches matching pattern(s) after confirmation."
    )
    parser_fade.add_argument(
        "patterns", nargs="+", help="One or more patterns to match branch names against."
    ).completer = branch_completer
    parser_fade.set_defaults(
        func=lambda args: core.fade_branches(
            args.patterns, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- clean command ---
    parser_clean = subparsers.add_parser(
        "clean",
        help="Delete worktrees and/or associated branches matching pattern(s).",
    )
    parser_clean.add_argument(
        "branch_patterns",
        nargs="*",
        default=[],
        help="Optional branch pattern(s) to select what to clean. Defaults to all output branches.",
    ).completer = branch_completer
    clean_group = parser_clean.add_mutually_exclusive_group()
    clean_group.add_argument(
        "--soft",
        action="store_true",
        help="Only delete worktrees, not the branches.",
    )
    clean_group.add_argument(
        "--hard",
        action="store_true",
        help="Delete both worktrees and branches (default).",
    )
    parser_clean.set_defaults(
        func=lambda args: core.clean_worktrees(
            branch_patterns=args.branch_patterns,
            mode="soft" if args.soft else "hard",
            show_cmd_output=(args.verbose >= 2),
        )
    )

    # --- surrender command ---
    parser_surrender = subparsers.add_parser(
        "surrender", help="Kill running agent processes."
    )
    parser_surrender.add_argument(
        "branch_patterns",
        nargs="*",
        default=[],
        help="Optional branch pattern(s) to select worktrees. Defaults to all.",
    ).completer = branch_completer
    parser_surrender.set_defaults(
        func=lambda args: core.surrender(
            args.branch_patterns, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- state command ---
    parser_state = subparsers.add_parser(
        "state", help="Show the state of existing worktrees."
    )
    parser_state.add_argument(
        "branch_pattern",
        nargs="*",
        default=[],
        help="Optional glob-style pattern(s) to filter branches by name.",
    ).completer = branch_completer
    parser_state.set_defaults(
        func=lambda args: core.state(
            branch_patterns=args.branch_pattern, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- task command ---
    parser_task = subparsers.add_parser(
        "task", help="Create a new task spec file and open it in your editor."
    )
    parser_task.add_argument(
        "task_name",
        nargs="?",
        default=None,
        help="The name of the task file (without .md extension).",
    )
    parser_task.set_defaults(
        func=lambda args: core.create_task_file(
            task_name=args.task_name, show_cmd_output=(args.verbose >= 2)
        )
    )

    # --- help command ---
    parser_help = subparsers.add_parser("help", help="Show this help message.")
    parser_help.set_defaults(func=lambda args: parser.print_help())

    argcomplete.autocomplete(parser)

    try:
        args, unknown_args = parser.parse_known_args()

        if args.command == "diff":
            # Reconstruct raw args after 'diff' to support '--' pathspec passthrough
            try:
                diff_idx = sys.argv.index("diff") + 1
                tail = sys.argv[diff_idx:]
            except ValueError:
                tail = []

            # Split on '--' to separate pathspec (after) from patterns/options (before)
            if "--" in tail:
                dd_i = tail.index("--")
                before_dd = tail[:dd_i]
                after_dd = tail[dd_i + 1 :]
            else:
                before_dd = tail
                after_dd = []

            # Extract branch patterns from the start until the first option
            branch_patterns = []
            diff_opts = []
            reached_opts = False
            for tok in before_dd:
                if not reached_opts and not tok.startswith("-"):
                    branch_patterns.append(tok)
                else:
                    reached_opts = True
                    diff_opts.append(tok)

            if after_dd:
                diff_opts.extend(["--"] + after_dd)

            # Override parsed values
            args.branch_patterns = branch_patterns
            args.diff_opts = diff_opts
        elif unknown_args:
            parser.error(f"unrecognized arguments: {' '.join(unknown_args)}")

        # Setup logging
        if args.quiet:
            log_level = logging.WARNING
        elif args.verbose >= 1:
            log_level = logging.DEBUG
        else:  # verbose == 0
            log_level = logging.INFO

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
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
