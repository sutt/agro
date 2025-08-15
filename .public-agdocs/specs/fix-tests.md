Fix the failing tests fromt he previous commit:

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 71 items

tests/test_cli.py ..............................                         [ 42%]
tests/test_core.py ........................................F             [100%]

=================================== FAILURES ===================================
____________________ test_muster_command_timeout_overrides _____________________

mock_run_command = <MagicMock name='_run_command' id='140541302068896'>
mock_get_worktree_state = <MagicMock name='get_worktree_state' id='140541304373328'>
mock_get_indices = <MagicMock name='_get_indices_from_branch_patterns' id='140541307129872'>
mock_config = <MagicMock name='config' id='140541304001152'>
mock_path = <MagicMock name='Path' id='140541304012480'>

    @patch("agro.core.Path")
    @patch("agro.core.config")
    @patch("agro.core._get_indices_from_branch_patterns", return_value=[1])
    @patch("agro.core.get_worktree_state", return_value={"t1": "b1"})
    @patch("agro.core._run_command")
    def test_muster_command_timeout_overrides(
        mock_run_command,
        mock_get_worktree_state,
        mock_get_indices,
        mock_config,
        mock_path,
    ):
        mock_path.return_value.is_dir.return_value = True
        mock_config.MUSTER_DEFAULT_TIMEOUT = 20
        mock_config.MUSTER_COMMON_CMDS = {
            "default_timeout": {"cmd": "cmd1"},
            "custom_timeout": {"cmd": "cmd2", "timeout": 10},
            "no_timeout": {"cmd": "cmd3", "timeout": 0},
            "null_timeout": {"cmd": "cmd4", "timeout": None},
        }
    
        # 1. Default timeout from config
        core.muster_command(command_str="some-cmd", branch_patterns=["b1"])
        mock_run_command.assert_called_with(
            ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=20
        )
    
        # 2. Common command with default timeout
        core.muster_command(command_str=None, common_cmd_key="default_timeout", branch_patterns=["b1"])
        mock_run_command.assert_called_with(
            ["cmd1"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=20
        )
    
        # 3. Common command with custom timeout
        core.muster_command(command_str=None, common_cmd_key="custom_timeout", branch_patterns=["b1"])
        mock_run_command.assert_called_with(
            ["cmd2"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=10
        )
    
        # 4. Common command with timeout: 0
        core.muster_command(command_str=None, common_cmd_key="no_timeout", branch_patterns=["b1"])
>       mock_run_command.assert_called_with(
            ["cmd3"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=20
        )

tests/test_core.py:665: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <MagicMock name='_run_command' id='140541302068896'>, args = (['cmd3'],)
kwargs = {'cwd': "<MagicMock name='Path().__truediv__()' id='140541304005952'>", 'shell': False, 'show_cmd_output': True, 'timeout': 20}
expected = call(['cmd3'], cwd="<MagicMock name='Path().__truediv__()' id='140541304005952'>", shell=False, show_cmd_output=True, timeout=20)
actual = call(['cmd3'], cwd="<MagicMock name='Path().__truediv__()' id='140541304005952'>", shell=False, show_cmd_output=True, timeout=None)
_error_message = <function NonCallableMock.assert_called_with.<locals>._error_message at 0x7fd2528168e0>
cause = None

    def assert_called_with(self, /, *args, **kwargs):
        """assert that the last call was made with the specified arguments.
    
        Raises an AssertionError if the args and keyword args passed in are
        different to the last call to the mock."""
        if self.call_args is None:
            expected = self._format_mock_call_signature(args, kwargs)
            actual = 'not called.'
            error_message = ('expected call not found.\nExpected: %s\n  Actual: %s'
                    % (expected, actual))
            raise AssertionError(error_message)
    
        def _error_message():
            msg = self._format_mock_failure_message(args, kwargs)
            return msg
        expected = self._call_matcher(_Call((args, kwargs), two=True))
        actual = self._call_matcher(self.call_args)
        if actual != expected:
            cause = expected if isinstance(expected, Exception) else None
>           raise AssertionError(_error_message()) from cause
E           AssertionError: expected call not found.
E           Expected: _run_command(['cmd3'], cwd="<MagicMock name='Path().__truediv__()' id='140541304005952'>", shell=False, show_cmd_output=True, timeout=20)
E             Actual: _run_command(['cmd3'], cwd="<MagicMock name='Path().__truediv__()' id='140541304005952'>", shell=False, show_cmd_output=True, timeout=None)

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:949: AssertionError
=========================== short test summary info ============================
FAILED tests/test_core.py::test_muster_command_timeout_overrides - AssertionE...
========================= 1 failed, 70 passed in 0.11s =========================
