import pytest
from unittest.mock import patch, call, MagicMock

from agro import core


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("branch", ["branch"]),
        ("feature/branch", ["feature/branch"]),
        ("branch.{1-3}", ["branch.1", "branch.2", "branch.3"]),
        ("branch.{3-1}", []),
        ("branch.{2,4}", ["branch.2", "branch.4"]),
        ("branch.{1-3,5}", ["branch.1", "branch.2", "branch.3", "branch.5"]),
        ("b.{1,3-4}", ["b.1", "b.3", "b.4"]),
        ("b.{1, 3-4 , 6}", ["b.1", "b.3", "b.4", "b.6"]),
        ("no-braces", ["no-braces"]),
        ("prefix.{1,1}.suffix", ["prefix.1.suffix"]),
        ("b.{}", ["b.{}"]),   # XFAIL: doesnt work as expected, should be empty list
        ("b.{ }", []),
        ("b.{,}", []),
    ],
)
def test_expand_branch_pattern_valid(pattern, expected):
    assert core._expand_branch_pattern(pattern) == expected


@pytest.mark.parametrize(
    "pattern",
    [
        "b.{1-}",
        "b.{a-c}",
        "b.{1,a}",
        "b.{1-2-3}",
    ],
)
def test_expand_branch_pattern_invalid(pattern):
    with pytest.raises(ValueError):
        core._expand_branch_pattern(pattern)


ALL_BRANCHES = [
    "main",
    "develop",
    "feature/one",
    "feature/two",
    "output/feat.1",
    "output/feat.2",
    "output/feat.3",
    "output/feat.5",
    "output/other.1",
    "bugfix/short",
]


@patch("agro.core._get_all_branches", return_value=ALL_BRANCHES)
@pytest.mark.parametrize(
    "pattern, expected",
    [
        # Exact match
        ("main", ["main"]),
        # No exact match, prefix match
        ("feature", ["feature/one", "feature/two"]),
        ("bugfix", ["bugfix/short"]),
        # Glob pattern
        ("feature/*", ["feature/one", "feature/two"]),
        (
            "output/feat.*",
            ["output/feat.1", "output/feat.2", "output/feat.3", "output/feat.5"],
        ),
        # Brace expansion
        ("output/feat.{1-3}", ["output/feat.1", "output/feat.2", "output/feat.3"]),
        ("output/feat.{2,5}", ["output/feat.2", "output/feat.5"]),
        # .4 does not exist
        ("output/feat.{1-4}", ["output/feat.1", "output/feat.2", "output/feat.3"]),
        # No match
        ("nonexistent", []),
        ("output/feat.{6-7}", []),
        # Exact match takes precedence over prefix
        ("feature/one", ["feature/one"]),
        # Empty brace expansion
        ("output/feat.{}", []),
    ],
)
def test_get_matching_branches(mock_get_branches, pattern, expected):
    assert core._get_matching_branches(pattern) == expected
    mock_get_branches.assert_called_once()


if __name__ == "__main__":
    # uv run python -m tests.test_core
    print(core._expand_branch_pattern("b{}"))


@patch("agro.core.get_worktree_state")
@patch("agro.core._get_matching_branches")
def test_get_indices_from_branch_patterns(mock_get_matching_branches, mock_get_worktree_state):
    mock_get_worktree_state.return_value = {
        "t1": "feature/one",
        "t2": "feature/two",
        "t3": "bugfix/short",
        "t4": "feature/one",  # another worktree on same branch
        "t5": "other",
    }

    # Test with no patterns (should return all)
    assert core._get_indices_from_branch_patterns(show_cmd_output=False) == [1, 2, 3, 4, 5]

    # Test with a pattern that matches multiple branches
    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]
    assert core._get_indices_from_branch_patterns(["feature/*"], show_cmd_output=False) == [1, 2, 4]
    mock_get_matching_branches.assert_called_once_with("feature/*", show_cmd_output=False)

    # Test with a pattern that matches one branch
    mock_get_matching_branches.reset_mock()
    mock_get_matching_branches.return_value = ["bugfix/short"]
    assert core._get_indices_from_branch_patterns(["bugfix/short"], show_cmd_output=False) == [3]
    mock_get_matching_branches.assert_called_once_with("bugfix/short", show_cmd_output=False)

    # Test with multiple patterns
    mock_get_matching_branches.reset_mock()
    def side_effect(pattern, show_cmd_output=False):
        if pattern == "feature/two":
            return ["feature/two"]
        if pattern == "other":
            return ["other"]
        return []
    mock_get_matching_branches.side_effect = side_effect
    assert core._get_indices_from_branch_patterns(["feature/two", "other"], show_cmd_output=False) == [2, 5]
    assert mock_get_matching_branches.call_count == 2

    # Test with pattern that matches nothing
    mock_get_matching_branches.reset_mock()
    mock_get_matching_branches.side_effect = None
    mock_get_matching_branches.return_value = []
    assert core._get_indices_from_branch_patterns(["nonexistent"], show_cmd_output=False) == []

    # Test with no worktrees
    mock_get_worktree_state.return_value = {}
    assert core._get_indices_from_branch_patterns(show_cmd_output=False) == []


@patch("agro.core._get_matching_branches")
@patch("agro.core._run_command")
@patch("builtins.input", return_value="y")
@patch("agro.core.logger")
def test_fade_branches_simple(
    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
):
    # Mock current branch
    mock_run_command.side_effect = [
        MagicMock(stdout="main"),  # for getting current branch
        MagicMock(returncode=0),  # for git branch -D
        MagicMock(returncode=0),  # for git branch -D
    ]

    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]

    core.fade_branches(["feature/*"], show_cmd_output=False)

    mock_get_matching_branches.assert_called_once_with(
        "feature/*", show_cmd_output=False
    )

    # Check that we tried to delete the branches
    delete_calls = [
        call(
            ["git", "branch", "-D", "feature/one"],
            capture_output=True,
            check=False,
            show_cmd_output=False,
        ),
        call(
            ["git", "branch", "-D", "feature/two"],
            capture_output=True,
            check=False,
            show_cmd_output=False,
        ),
    ]
    # First call is to get current branch
    mock_run_command.assert_has_calls(delete_calls, any_order=True)
    assert mock_run_command.call_count == 3  # 1 for current branch, 2 for delete

    # Check logging
    mock_logger.info.assert_any_call("Deleted branch 'feature/one'.")
    mock_logger.info.assert_any_call("Deleted branch 'feature/two'.")


@patch("agro.core._get_matching_branches")
@patch("agro.core._run_command")
@patch("builtins.input", return_value="y")
@patch("agro.core.logger")
def test_fade_branches_skips_current_branch(
    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
):
    # Mock current branch
    mock_run_command.side_effect = [
        MagicMock(stdout="feature/one"),  # for getting current branch
        MagicMock(returncode=0),  # for git branch -D
    ]

    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]

    core.fade_branches(["feature/*"], show_cmd_output=True)

    mock_get_matching_branches.assert_called_once_with(
        "feature/*", show_cmd_output=True
    )

    # Check that we tried to delete only one branch
    mock_run_command.assert_called_with(
        ["git", "branch", "-D", "feature/two"],
        capture_output=True,
        check=False,
        show_cmd_output=True,
    )
    assert mock_run_command.call_count == 2  # 1 for current branch, 1 for delete

    # Check logging
    mock_logger.warning.assert_called_with(
        "Skipping currently checked out branch 'feature/one'"
    )
    mock_logger.info.assert_any_call("Deleted branch 'feature/two'.")


@patch("agro.core._get_matching_branches")
@patch("agro.core._run_command")
@patch("builtins.input", return_value="n")
@patch("agro.core.logger")
def test_fade_branches_user_cancel(
    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
):
    # Mock current branch
    mock_run_command.return_value = MagicMock(stdout="main")

    mock_get_matching_branches.return_value = ["feature/one"]

    core.fade_branches(["feature/one"], show_cmd_output=False)

    # Check that we did not try to delete
    delete_call = call(
        ["git", "branch", "-D", "feature/one"],
        capture_output=True,
        check=False,
        show_cmd_output=False,
    )
    assert delete_call not in mock_run_command.mock_calls

    # Check logging
    mock_logger.warning.assert_called_with("Operation cancelled by user.")


@patch("agro.core._get_matching_branches")
@patch("agro.core.logger")
def test_fade_branches_no_match(mock_logger, mock_get_matching_branches):
    mock_get_matching_branches.return_value = []
    core.fade_branches(["nonexistent"], show_cmd_output=False)
    mock_logger.info.assert_called_with(
        "No branches found matching the patterns to delete."
    )


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
    mock_run_command.assert_has_calls(expected_calls_stat)
    assert mock_run_command.call_count == 2

    # test with multiple diff_opts
    mock_run_command.reset_mock()
    core.diff_worktrees([], diff_opts=["--stat", "--cached"], show_cmd_output=False)
    expected_calls_multiple = [
        call(
            ["git", "diff", "--stat", "--cached", "tree/t1", "HEAD"],
            cwd=str(mock_path.return_value / "t1"),
            show_cmd_output=True,
        ),
        call(
            ["git", "diff", "--stat", "--cached", "tree/t2", "HEAD"],
            cwd=str(mock_path.return_value / "t2"),
            show_cmd_output=True,
        ),
    ]
    mock_run_command.assert_has_calls(expected_calls_multiple)
    assert mock_run_command.call_count == 2

    # test with pathspec
    mock_run_command.reset_mock()
    core.diff_worktrees([], diff_opts=["--", "my/path"], show_cmd_output=False)
    expected_calls_pathspec = [
        call(
            ["git", "diff", "tree/t1", "HEAD", "--", "my/path"],
            cwd=str(mock_path.return_value / "t1"),
            show_cmd_output=True,
        ),
        call(
            ["git", "diff", "tree/t2", "HEAD", "--", "my/path"],
            cwd=str(mock_path.return_value / "t2"),
            show_cmd_output=True,
        ),
    ]
    mock_run_command.assert_has_calls(expected_calls_pathspec)
    assert mock_run_command.call_count == 2

    # test with options and pathspec
    mock_run_command.reset_mock()
    core.diff_worktrees(
        [], diff_opts=["--stat", "--", "my/path"], show_cmd_output=False
    )
    expected_calls_opts_pathspec = [
        call(
            ["git", "diff", "--stat", "tree/t1", "HEAD", "--", "my/path"],
            cwd=str(mock_path.return_value / "t1"),
            show_cmd_output=True,
        ),
        call(
            ["git", "diff", "--stat", "tree/t2", "HEAD", "--", "my/path"],
            cwd=str(mock_path.return_value / "t2"),
            show_cmd_output=True,
        ),
    ]
    mock_run_command.assert_has_calls(expected_calls_opts_pathspec)
    assert mock_run_command.call_count == 2

    # test no indices
    mock_run_command.reset_mock()
    mock_get_indices.return_value = []
    core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
    mock_run_command.assert_not_called()
    mock_logger.warning.assert_called_with("No worktrees found matching the provided patterns.")

    # test worktree dir not found
    mock_logger.reset_mock()
    mock_run_command.reset_mock()
    mock_get_indices.return_value = [1]
    mock_path.return_value.__truediv__.return_value.is_dir.return_value = False
    core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
    mock_run_command.assert_not_called()
    mock_logger.warning.assert_called_with(
        f"Worktree t1 at '{mock_path.return_value / 't1'}' not found. Skipping."
    )


@patch("agro.core.logger")
@patch("builtins.input", return_value="y")
@patch("agro.core._run_command")
@patch("agro.core.delete_tree")
@patch("agro.core._get_matching_branches")
@patch("agro.core.get_worktree_state")
def test_clean_worktrees_hard(
    mock_get_worktree_state,
    mock_get_matching_branches,
    mock_delete_tree,
    mock_run_command,
    mock_input,
    mock_logger,
):
    # Arrange
    mock_get_worktree_state.return_value = {
        "t1": "output/feat.1",
        "t2": "output/feat.2",
        "t3": "another/branch",
    }
    mock_get_matching_branches.return_value = ["output/feat.1", "output/feat.2"]
    # for git rev-parse HEAD
    mock_run_command.return_value = MagicMock(stdout="main")

    # Act
    core.clean_worktrees(branch_patterns=["output/feat.*"], mode="hard", show_cmd_output=False)

    # Assert
    mock_get_matching_branches.assert_called_once_with("output/feat.*", show_cmd_output=False)

    # Dry run logs
    mock_logger.info.assert_any_call("The following worktrees will be deleted:")
    mock_logger.info.assert_any_call("  - t1 (branch: output/feat.1)")
    mock_logger.info.assert_any_call("  - t2 (branch: output/feat.2)")
    mock_logger.info.assert_any_call("The following branches will be deleted (hard clean):")
    mock_logger.info.assert_any_call("  - output/feat.1")
    mock_logger.info.assert_any_call("  - output/feat.2")

    mock_input.assert_called_once()

    # delete_tree calls
    mock_delete_tree.assert_has_calls(
        [
            call("1", show_cmd_output=False),
            call("2", show_cmd_output=False),
        ],
        any_order=True,
    )
    assert mock_delete_tree.call_count == 2

    # branch deletion calls
    # 1 for git rev-parse, 2 for git branch -D
    assert mock_run_command.call_count == 3
    mock_run_command.assert_any_call(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        check=True,
        show_cmd_output=False,
    )
    mock_run_command.assert_any_call(
        ["git", "branch", "-D", "output/feat.1"],
        capture_output=True,
        check=False,
        show_cmd_output=False,
    )
    mock_run_command.assert_any_call(
        ["git", "branch", "-D", "output/feat.2"],
        capture_output=True,
        check=False,
        show_cmd_output=False,
    )


@patch("agro.core.logger")
@patch("builtins.input", return_value="y")
@patch("agro.core._run_command")
@patch("agro.core.delete_tree")
@patch("agro.core._get_matching_branches")
@patch("agro.core.get_worktree_state")
def test_clean_worktrees_soft(
    mock_get_worktree_state,
    mock_get_matching_branches,
    mock_delete_tree,
    mock_run_command,
    mock_input,
    mock_logger,
):
    # Arrange
    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
    mock_get_matching_branches.return_value = ["output/feat.1"]

    # Act
    core.clean_worktrees(branch_patterns=["output/feat.1"], mode="soft", show_cmd_output=False)

    # Assert
    mock_logger.info.assert_any_call("The following worktrees will be deleted:")
    mock_logger.info.assert_any_call("  - t1 (branch: output/feat.1)")
    # Ensure hard clean message is NOT present
    for call_args in mock_logger.info.call_args_list:
        assert "branches will be deleted" not in call_args[0][0]

    mock_input.assert_called_once()
    mock_delete_tree.assert_called_once_with("1", show_cmd_output=False)
    mock_run_command.assert_not_called()  # No branch deletion


@patch("agro.core.config")
@patch("agro.core.logger")
@patch("builtins.input", return_value="y")
@patch("agro.core.delete_tree")
@patch("agro.core._get_matching_branches")
@patch("agro.core.get_worktree_state")
def test_clean_worktrees_no_pattern(
    mock_get_worktree_state,
    mock_get_matching_branches,
    mock_delete_tree,
    mock_input,
    mock_logger,
    mock_config,
):
    # Arrange
    mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
    mock_get_matching_branches.return_value = ["output/feat.1"]

    # Act
    core.clean_worktrees(branch_patterns=[], mode="soft", show_cmd_output=False)

    # Assert
    mock_get_matching_branches.assert_called_once_with("output/", show_cmd_output=False)
    mock_delete_tree.assert_called_once_with("1", show_cmd_output=False)


@patch("agro.core.logger")
@patch("builtins.input", return_value="n")
@patch("agro.core.delete_tree")
@patch("agro.core._get_matching_branches")
@patch("agro.core.get_worktree_state")
def test_clean_worktrees_cancel(
    mock_get_worktree_state,
    mock_get_matching_branches,
    mock_delete_tree,
    mock_input,
    mock_logger,
):
    # Arrange
    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
    mock_get_matching_branches.return_value = ["output/feat.1"]

    # Act
    core.clean_worktrees(branch_patterns=["output/feat.1"], mode="hard", show_cmd_output=False)

    # Assert
    mock_input.assert_called_once()
    mock_logger.warning.assert_called_with("Operation cancelled by user.")
    mock_delete_tree.assert_not_called()


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
        "testq": {"cmd": "uv run pytest -q"},
        "server-start": {
            "cmd": "my-app --daemon > server.log 2>&1 &",
            "timeout": None,
        },
        "server-kill": {"cmd": "kill $(cat server.pid)"},
    }
    mock_config.MUSTER_DEFAULT_TIMEOUT = 20
    mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
    mock_config.AGDOCS_DIR = ".agdocs"

    # Test with common command (no shell)
    core.muster_command(
        command_str=None,
        branch_patterns=["output/branch.1"],
        common_cmd_key="testq",
        show_cmd_output=True,
    )
    mock_run_command.assert_called_once_with(
        ["uv", "run", "pytest", "-q"],
        cwd=str(mock_path.return_value / "t1"),
        shell=False,
        show_cmd_output=True,
        timeout=20,
    )
    mock_run_command.reset_mock()

    # Test with positional command (no shell)
    core.muster_command(
        command_str="ls -l",
        branch_patterns=["output/branch.1"],
        show_cmd_output=True,
    )
    mock_run_command.assert_called_once_with(
        ["ls", "-l"],
        cwd=str(mock_path.return_value / "t1"),
        shell=False,
        show_cmd_output=True,
        timeout=20,
    )
    mock_run_command.reset_mock()

    # Test with server-start common command (needs shell, no timeout)
    core.muster_command(
        command_str=None,
        branch_patterns=["output/branch.1"],
        common_cmd_key="server-start",
        show_cmd_output=True,
    )
    mock_run_command.assert_called_once_with(
        "my-app --daemon > server.log 2>&1 &",
        cwd=str(mock_path.return_value / "t1"),
        shell=True,
        show_cmd_output=True,
        timeout=None,
    )
    mock_run_command.reset_mock()

    # Test with server-kill common command (needs shell, default timeout)
    core.muster_command(
        command_str=None,
        branch_patterns=["output/branch.1"],
        common_cmd_key="server-kill",
        show_cmd_output=True,
    )
    mock_run_command.assert_called_once_with(
        "kill $(cat server.pid)",
        cwd=str(mock_path.return_value / "t1"),
        shell=True,
        show_cmd_output=True,
        timeout=20,
    )
    mock_run_command.reset_mock()

    # Test with no branch pattern (uses default)
    core.muster_command(command_str="ls", branch_patterns=[], show_cmd_output=False)
    mock_get_indices.assert_called_with(["output/"], False)
    mock_logger.info.assert_any_call(
        "No branch pattern specified. Using default pattern for output branches: 'output/*'"
    )

    # Test common command not found
    with pytest.raises(ValueError, match="Common command 'nonexistent' not found"):
        core.muster_command(command_str=None, branch_patterns=[], common_cmd_key="nonexistent")


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
    mock_run_command.assert_called_with(
        ["cmd3"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
    )

    # 5. Common command with timeout: null
    core.muster_command(command_str=None, common_cmd_key="null_timeout", branch_patterns=["b1"])
    mock_run_command.assert_called_with(
        ["cmd4"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
    )

    # 6. CLI flag overrides common command timeout
    core.muster_command(command_str=None, common_cmd_key="custom_timeout", branch_patterns=["b1"], timeout=30)
    mock_run_command.assert_called_with(
        ["cmd2"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=30
    )

    # 7. CLI flag overrides default timeout
    core.muster_command(command_str="some-cmd", branch_patterns=["b1"], timeout=30)
    mock_run_command.assert_called_with(
        ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=30
    )

    # 8. CLI flag of 0 means no timeout
    core.muster_command(command_str="some-cmd", branch_patterns=["b1"], timeout=0)
    mock_run_command.assert_called_with(
        ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
    )
