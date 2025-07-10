Fix the tests:

Here's the debug log

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 28 items

tests/test_cli.py ..........FFFFFFFF....F.FFFF                           [100%]

=================================== FAILURES ===================================
__________________________ test_dispatch_exec_simple ___________________________

mock_find = <MagicMock name='find_task_file' id='140434272984560'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434274636656'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271289712'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_simple(mock_find, mock_find_recent, mock_exec_agent):
        """Test exec with just a taskfile."""
        mock_find.return_value = Path("task.md")
        args = argparse.Namespace(
            agent_args=["task.md"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
_________________ test_dispatch_exec_with_num_trees_positional _________________

mock_find = <MagicMock name='find_task_file' id='140434271302624'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271138544'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434285650736'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_num_trees_positional(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with taskfile and num_trees positional arg."""
        mock_find.return_value = Path("task.md")
        args = argparse.Namespace(
            agent_args=["task.md", "3"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:80: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', '3'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
_________________ test_dispatch_exec_with_exec_cmd_positional __________________

mock_find = <MagicMock name='find_task_file' id='140434271598832'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434272544112'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271598160'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_exec_cmd_positional(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with taskfile and exec_cmd positional arg."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        args = argparse.Namespace(
            agent_args=["task.md", "my-agent"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:113: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', 'my-agent'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
__________ test_dispatch_exec_with_num_trees_and_exec_cmd_positional ___________

mock_find = <MagicMock name='find_task_file' id='140434271677104'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271672880'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271677056'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_num_trees_and_exec_cmd_positional(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with taskfile, num_trees, and exec_cmd positional args."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        args = argparse.Namespace(
            agent_args=["task.md", "3", "my-agent", "--agent-opt"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=True,
            no_env_overrides=True,
            verbose=2,
        )
>       _dispatch_exec(args)

tests/test_cli.py:147: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', '3', 'my-agent', '--agent-opt'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=True, no_env_overrides=True, verbose=2)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
_________ test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2 __________

mock_find = <MagicMock name='find_task_file' id='140434271707904'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271703776'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271708000'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with taskfile, num_trees, and exec_cmd positional args swapped."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        args = argparse.Namespace(
            agent_args=["task.md", "my-agent", "3", "--agent-opt"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=True,
            no_env_overrides=True,
            verbose=2,
        )
>       _dispatch_exec(args)

tests/test_cli.py:179: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', 'my-agent', '3', '--agent-opt'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=True, no_env_overrides=True, verbose=2)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
___________________ test_dispatch_exec_with_num_trees_option ___________________

mock_find = <MagicMock name='find_task_file' id='140434271714864'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271653184'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271657120'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_num_trees_option(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with -n option for num_trees."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        args = argparse.Namespace(
            agent_args=["task.md", "my-agent", "--agent-opt"],
            num_trees_opt=3,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:211: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', 'my-agent', '--agent-opt'], num_trees_opt=3, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
_________________ test_dispatch_exec_with_tree_indices_option __________________

mock_find = <MagicMock name='find_task_file' id='140434271711072'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271706608'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271702144'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_tree_indices_option(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with -t option for tree_indices."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        args = argparse.Namespace(
            agent_args=["task.md", "my-agent", "--agent-opt"],
            num_trees_opt=None,
            tree_indices="1,2,3",
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:243: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', 'my-agent', '--agent-opt'], num_trees_opt=None, tree_indices='1,2,3', exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
___________________ test_dispatch_exec_with_exec_cmd_option ____________________

mock_find = <MagicMock name='find_task_file' id='140434271672112'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434276494144'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271672304'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_exec_cmd_option(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with -c option for exec_cmd."""
        mock_find.return_value = Path("task.md")
        args = argparse.Namespace(
            agent_args=["task.md", "--agent-opt"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt="my-agent",
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:275: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', '--agent-opt'], num_trees_opt=None, tree_indices=None, exec_cmd_opt='my-agent', agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
____________ test_dispatch_exec_no_taskfile_use_recent_confirm_yes _____________

mock_find = <MagicMock name='find_task_file' id='140434271599504'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434274514656'>
mock_input = <MagicMock name='input' id='140434271715008'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434278216576'>

    @patch("agro.cli.core.exec_agent")
    @patch("builtins.input", return_value="y")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=Path("recent.md"))
    @patch("agro.cli.core.find_task_file", return_value=None)
    def test_dispatch_exec_no_taskfile_use_recent_confirm_yes(
        mock_find, mock_find_recent, mock_input, mock_exec_agent
    ):
        """Test using recent taskfile when user confirms."""
        args = argparse.Namespace(
            agent_args=[],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:377: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=[], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
__________________ test_dispatch_exec_with_agent_type_option ___________________

mock_find = <MagicMock name='find_task_file' id='140434271667456'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271664944'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271633488'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_with_agent_type_option(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test exec with -a option for agent_type."""
        mock_find.return_value = Path("task.md")
        args = argparse.Namespace(
            agent_args=["task.md"],
            num_trees_opt=None,
            tree_indices=None,
            exec_cmd_opt=None,
            agent_type_opt="gemini",
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
        )
>       _dispatch_exec(args)

tests/test_cli.py:433: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt='gemini', fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
______________ test_dispatch_exec_infer_agent_type_from_exec_cmd _______________

mock_find = <MagicMock name='find_task_file' id='140434271141136'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434274513600'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434274638192'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_infer_agent_type_from_exec_cmd(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test agent_type is inferred from exec_cmd."""
        mock_find.return_value = Path("task.md")
        with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}}):
            args = argparse.Namespace(
                agent_args=["task.md"],
                num_trees_opt=None,
                tree_indices=None,
                exec_cmd_opt="my-gemini-agent",
                agent_type_opt=None,
                fresh_env=False,
                no_env_overrides=False,
                verbose=0,
            )
>           _dispatch_exec(args)

tests/test_cli.py:466: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md'], num_trees_opt=None, tree_indices=None, exec_cmd_opt='my-gemini-agent', agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
_________ test_dispatch_exec_infer_agent_type_from_positional_exec_cmd _________

mock_find = <MagicMock name='find_task_file' id='140434271663648'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271134944'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434274632048'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_infer_agent_type_from_positional_exec_cmd(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test agent_type is inferred from positional exec_cmd."""
        mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
        with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}}):
            args = argparse.Namespace(
                agent_args=["task.md", "my-gemini-agent"],
                num_trees_opt=None,
                tree_indices=None,
                exec_cmd_opt=None,
                agent_type_opt=None,
                fresh_env=False,
                no_env_overrides=False,
                verbose=0,
            )
>           _dispatch_exec(args)

tests/test_cli.py:499: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md', 'my-gemini-agent'], num_trees_opt=None, tree_indices=None, exec_cmd_opt=None, agent_type_opt=None, fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
______________ test_dispatch_exec_no_inference_when_both_provided ______________

mock_find = <MagicMock name='find_task_file' id='140434271291536'>
mock_find_recent = <MagicMock name='find_most_recent_task_file' id='140434271588032'>
mock_exec_agent = <MagicMock name='exec_agent' id='140434271587264'>

    @patch("agro.cli.core.exec_agent")
    @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
    @patch("agro.cli.core.find_task_file")
    def test_dispatch_exec_no_inference_when_both_provided(
        mock_find, mock_find_recent, mock_exec_agent
    ):
        """Test no inference occurs when both agent_type and exec_cmd are provided."""
        mock_find.return_value = Path("task.md")
        with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}, "aider": {}}):
            args = argparse.Namespace(
                agent_args=["task.md"],
                num_trees_opt=None,
                tree_indices=None,
                exec_cmd_opt="my-gemini-agent",
                agent_type_opt="aider",
                fresh_env=False,
                no_env_overrides=False,
                verbose=0,
            )
>           _dispatch_exec(args)

tests/test_cli.py:532: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(agent_args=['task.md'], num_trees_opt=None, tree_indices=None, exec_cmd_opt='my-gemini-agent', agent_type_opt='aider', fresh_env=False, no_env_overrides=False, verbose=0)

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
                if args.tree_indices is not None:
                    raise ValueError(
                        "Cannot specify number of trees positionally and with -t/--tree-indices."
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
            indices_str=args.tree_indices,
            num_trees=num_trees,
            show_cmd_output=(args.verbose >= 2),
            agent_type=agent_type,
>           auto_commit=not args.no_auto_commit,
                            ^^^^^^^^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'no_auto_commit'

src/agro/cli.py:109: AttributeError
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_dispatch_exec_simple - AttributeError: 'Namesp...
FAILED tests/test_cli.py::test_dispatch_exec_with_num_trees_positional - Attr...
FAILED tests/test_cli.py::test_dispatch_exec_with_exec_cmd_positional - Attri...
FAILED tests/test_cli.py::test_dispatch_exec_with_num_trees_and_exec_cmd_positional
FAILED tests/test_cli.py::test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2
FAILED tests/test_cli.py::test_dispatch_exec_with_num_trees_option - Attribut...
FAILED tests/test_cli.py::test_dispatch_exec_with_tree_indices_option - Attri...
FAILED tests/test_cli.py::test_dispatch_exec_with_exec_cmd_option - Attribute...
FAILED tests/test_cli.py::test_dispatch_exec_no_taskfile_use_recent_confirm_yes
FAILED tests/test_cli.py::test_dispatch_exec_with_agent_type_option - Attribu...
FAILED tests/test_cli.py::test_dispatch_exec_infer_agent_type_from_exec_cmd
FAILED tests/test_cli.py::test_dispatch_exec_infer_agent_type_from_positional_exec_cmd
FAILED tests/test_cli.py::test_dispatch_exec_no_inference_when_both_provided
======================== 13 failed, 15 passed in 0.16s =========================
