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
