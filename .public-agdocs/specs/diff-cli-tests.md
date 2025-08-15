Fix the tests below (test logs section) and add extra tests for this functionality as described be the previous spec below:

Previous Spec: ----

Refactor the "agro diff" cli:

Enable agro diff [diff-opts] to pass through a path like "agro diff -- my/path that runs "git diff -- my/path"

Note for agro diff cli the cli hint says, showing both branch-patterns 
 diff [branch-patterns] [diff-opts]

From the git documentation on git diff we're looking to do this pattern
git diff [<options>] [<commit>] [--] [<path>...]

This means if you find a path argument in the diff-opts of the form "-- <some-path>" even within a larger string of args "... -- <some-path> ..." then the path stuff should go at the end of the git diff command string, but other args passed to the git diff (.e.g. --stat) should go in the git diff options place.

Here's some test cases and how they should work:

$ agro diff --stat -- tests
-> ['git', 'diff', '--stat', 'tree/t1', 'HEAD', '--', 'tests']
-> $ git diff --stat tree/t1 HEAD -- tests
-> applied to all worktrees that match the default pattern of "output/*"

$ agro diff -- tests
-> ['git', 'diff', 'tree/t1', 'HEAD', '--', 'tests']
-> $ git diff tree/t1 HEAD -- tests
-> applied to all worktrees that match the default pattern of "output/*"

agro diff --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees that match the default pattern of "output/*"

agro diff output/mything --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees that match the pattern of "output/mything*"

agro diff output/mything.{3,4} --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees of branches "output/mything.3", "output/mything.4"

Make it work for all these tests cases both.

Test Logs: ----

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 71 items

tests/test_cli.py ..............................                         [ 42%]
tests/test_core.py ..................................F......             [100%]

=================================== FAILURES ===================================
_____________________________ test_diff_worktrees ______________________________

mock_logger = <MagicMock name='logger' id='140089379284192'>
mock_run_command = <MagicMock name='_run_command' id='140089379312112'>
mock_get_worktree_state = <MagicMock name='get_worktree_state' id='140089379315904'>
mock_get_indices = <MagicMock name='_get_indices_from_branch_patterns' id='140089379319696'>
mock_path = <MagicMock name='Path' id='140089379323488'>

    @patch("agro.core.Path")
    @patch("agro.core._get_indices_from_branch_patterns")
    @patch("agro.core.get_worktree_state")
    @patch("agro.core._run_command")
    @patch("agro.core.logger")
    def test_diff_worktrees(
        mock_logger,
        mock_run_command,
        mock_get_worktree_state,
        mock_get_indices,
        mock_path,
    ):
        # setup
        mock_get_indices.return_value = [1, 2]
        mock_get_worktree_state.return_value = {
            "t1": "output/branch.1",
            "t2": "output/branch.2",
        }
        # Mock Path(...).is_dir() to return True
        mock_path.return_value.__truediv__.return_value.is_dir.return_value = True
    
        # test with no diff_opts
        core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
    
        mock_get_indices.assert_called_once()
        mock_get_worktree_state.assert_called_once()
    
        expected_calls = [
            call(
                ["git", "diff", "tree/t1", "HEAD"],
                cwd=str(mock_path.return_value / "t1"),
                show_cmd_output=True,
            ),
            call(
                ["git", "diff", "tree/t2", "HEAD"],
                cwd=str(mock_path.return_value / "t2"),
                show_cmd_output=True,
            ),
        ]
        mock_run_command.assert_has_calls(expected_calls)
        assert mock_run_command.call_count == 2
    
        # test with one diff_opt
        mock_run_command.reset_mock()
        core.diff_worktrees([], diff_opts=["--stat"], show_cmd_output=False)
        expected_calls_stat = [
            call(
                ["git", "diff", "--stat", "tree/t1", "HEAD"],
                cwd=str(mock_path.return_value / "t1"),
                show_cmd_output=True,
            ),
            call(
                ["git", "diff", "--stat", "tree/t2", "HEAD"],
                cwd=str(mock_path.return_value / "t2"),
                show_cmd_output=True,
            ),
        ]
>       mock_run_command.assert_has_calls(expected_calls_stat)

tests/test_core.py:321: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <MagicMock name='_run_command' id='140089379312112'>
calls = [call(['git', 'diff', '--stat', 'tree/t1', 'HEAD'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>"...--stat', 'tree/t2', 'HEAD'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>", show_cmd_output=True)]
any_order = False

    def assert_has_calls(self, calls, any_order=False):
        """assert the mock has been called with the specified calls.
        The `mock_calls` list is checked for the calls.
    
        If `any_order` is False (the default) then the calls must be
        sequential. There can be extra calls before or after the
        specified calls.
    
        If `any_order` is True then the calls can be in any order, but
        they must all appear in `mock_calls`."""
        expected = [self._call_matcher(c) for c in calls]
        cause = next((e for e in expected if isinstance(e, Exception)), None)
        all_calls = _CallList(self._call_matcher(c) for c in self.mock_calls)
        if not any_order:
            if expected not in all_calls:
                if cause is None:
                    problem = 'Calls not found.'
                else:
                    problem = ('Error processing expected calls.\n'
                               'Errors: {}').format(
                                   [e if isinstance(e, Exception) else None
                                    for e in expected])
>               raise AssertionError(
                    f'{problem}\n'
                    f'Expected: {_CallList(calls)}'
                    f'{self._calls_repr(prefix="  Actual").rstrip(".")}'
                ) from cause
E               AssertionError: Calls not found.
E               Expected: [call(['git', 'diff', '--stat', 'tree/t1', 'HEAD'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>", show_cmd_output=True),
E                call(['git', 'diff', '--stat', 'tree/t2', 'HEAD'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>", show_cmd_output=True)]
E                 Actual: [call(['git', 'diff', 'tree/t1', 'HEAD', '--stat'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>", show_cmd_output=True),
E                call(['git', 'diff', 'tree/t2', 'HEAD', '--stat'], cwd="<MagicMock name='Path().__truediv__()' id='140089379344352'>", show_cmd_output=True)]

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:986: AssertionError
=========================== short test summary info ============================
FAILED tests/test_core.py::test_diff_worktrees - AssertionError: Calls not fo...
========================= 1 failed, 70 passed in 0.16s =========================
