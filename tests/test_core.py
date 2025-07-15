import pytest
from unittest.mock import patch

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
