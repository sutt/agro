Fix the tests the kicked out on the previous commit:

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 70 items

tests/test_cli.py .........................F....                         [ 42%]
tests/test_core.py .......................................F              [100%]

=================================== FAILURES ===================================
_____________________________ test_dispatch_muster _____________________________

mock_muster_command = <MagicMock name='muster_command' id='139928195134240'>

    @patch("agro.cli.core.muster_command")
    def test_dispatch_muster(mock_muster_command):
        # Basic case: command and pattern
        args = argparse.Namespace(
            command_str="ls",
            branch_patterns=["p1"],
            common_cmd_key=None,
            verbose=0,
        )
>       _dispatch_muster(args)

tests/test_cli.py:480: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

args = Namespace(command_str='ls', branch_patterns=['p1'], common_cmd_key=None, verbose=0)

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
>           timeout=args.timeout,
                    ^^^^^^^^^^^^
        )
E       AttributeError: 'Namespace' object has no attribute 'timeout'

src/agro/cli.py:130: AttributeError
_____________________________ test_muster_command ______________________________

mock_logger = <MagicMock name='logger' id='139928190736032'>
mock_run_command = <MagicMock name='_run_command' id='139928188927632'>
mock_get_worktree_state = <MagicMock name='get_worktree_state' id='139928188980592'>
mock_get_indices = <MagicMock name='_get_indices_from_branch_patterns' id='139928188984528'>
mock_config = <MagicMock name='config' id='139928188988368'>
mock_path = <MagicMock name='Path' id='139928188923840'>

    @patch("agro.core.Path")
    @patch("agro.core.config")
    @patch("agro.core._get_indices_from_branch_patterns")
    @patch("agro.core.get_worktree_state")
    @patch("agro.core._run_command")
    @patch("agro.core.logger")
    def test_muster_command(
        mock_logger,
        mock_run_command,
        mock_get_worktree_state,
        mock_get_indices,
        mock_config,
        mock_path,
    ):
        # Arrange
        mock_get_indices.return_value = [1]
        mock_get_worktree_state.return_value = {"t1": "output/branch.1"}
        mock_path.return_value.is_dir.return_value = True
        mock_config.MUSTER_COMMON_CMDS = {
            "testq": "uv run pytest -q",
            "server-start": "my-app --daemon > server.log 2>&1 &",
            "server-kill": "kill $(cat server.pid)",
        }
        mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
        mock_config.AGDOCS_DIR = ".agdocs"
    
        # Test with common command (no shell)
>       core.muster_command(
            command_str=None,
            branch_patterns=["output/branch.1"],
            common_cmd_key="testq",
            show_cmd_output=True,
        )

tests/test_core.py:546: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

command_str = None, branch_patterns = ['output/branch.1']
show_cmd_output = True, common_cmd_key = 'testq', timeout = None

    def muster_command(
        command_str,
        branch_patterns,
        show_cmd_output=False,
        common_cmd_key=None,
        timeout=None,
    ):
        """Runs a command in multiple worktrees."""
        final_timeout = timeout  # CLI arg has highest precedence
    
        if common_cmd_key:
            cmd_data = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
            if not cmd_data or "cmd" not in cmd_data:
                config_path = Path(config.AGDOCS_DIR) / "conf" / "agro.conf.yml"
                msg = f"Common command '{common_cmd_key}' not found or is invalid in 'MUSTER_COMMON_CMDS'."
                if config_path.is_file():
                    msg += f" Check your config file at '{config_path}'."
                else:
                    msg += f" No config file found at '{config_path}'."
    
                available_cmds = ", ".join(sorted(config.MUSTER_COMMON_CMDS.keys()))
                if available_cmds:
                    msg += f" Available commands are: {available_cmds}."
    
>               raise ValueError(msg)
E               ValueError: Common command 'testq' not found or is invalid in 'MUSTER_COMMON_CMDS'. Check your config file at '<MagicMock name='Path().__truediv__().__truediv__()' id='139928205411104'>'. Available commands are: server-kill, server-start, testq.

src/agro/core.py:1006: ValueError
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_dispatch_muster - AttributeError: 'Namespace' ...
FAILED tests/test_core.py::test_muster_command - ValueError: Common command '...
========================= 2 failed, 68 passed in 0.18s =========================
