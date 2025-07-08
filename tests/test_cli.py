import argparse
from pathlib import Path
from unittest.mock import patch

import pytest

from agro.cli import _dispatch_exec, _is_indices_list


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("1", True),
        ("1,2,3", True),
        (" 1, 2 ,3 ", True),
        ("1,2,", True),
        ("", False),
        (",", False),
        (",,", False),
        ("a", False),
        ("1,a,3", False),
        ("1, 2, a", False),
    ],
)
def test_is_indices_list(input_str, expected):
    assert _is_indices_list(input_str) == expected


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_all_positional(mock_find, mock_exec):
    """Test exec with taskfile, num_trees, and exec_cmd as positional args."""
    mock_find.side_effect = [
        (Path("task.md"), False),  # Initial check
        (Path("task.md"), False),  # Final retrieval
    ]
    args = argparse.Namespace(
        agent_args=["task.md", "3", "my-agent", "--agent-opt"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=True,
        no_env_overrides=True,
        verbose=2,
    )
    _dispatch_exec(args)
    mock_exec.assert_called_once_with(
        task_file="task.md",
        fresh_env=True,
        no_overrides=True,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=True,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_swapped_positional(mock_find, mock_exec):
    """Test exec with swapped num_trees and exec_cmd positional args."""
    mock_find.side_effect = [(Path("task.md"), False), (Path("task.md"), False)]
    args = argparse.Namespace(
        agent_args=["task.md", "my-agent", "3", "--agent-opt"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_exec.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
@patch("builtins.input", return_value="y")
def test_dispatch_exec_auto_detect_taskfile(mock_input, mock_find, mock_exec):
    """Test exec with auto-detected taskfile, user confirms."""
    mock_find.return_value = (Path("specs/latest.md"), True)
    args = argparse.Namespace(
        agent_args=["3", "my-agent"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_with(None)
    mock_input.assert_called_once_with("Use most recent task file 'latest.md'? [Y/n]: ")
    mock_exec.assert_called_once_with(
        task_file="specs/latest.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
@patch("builtins.input", return_value="n")
def test_dispatch_exec_auto_detect_taskfile_denied(mock_input, mock_find, mock_exec):
    """Test exec with auto-detected taskfile, user denies."""
    mock_find.return_value = (Path("specs/latest.md"), True)
    args = argparse.Namespace(agent_args=[], exec_cmd_opt=None, num_trees_opt=None, tree_indices=None, fresh_env=False, no_env_overrides=False, verbose=0)
    _dispatch_exec(args)
    mock_exec.assert_not_called()


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_no_taskfile_found(mock_find, mock_exec):
    """Test FileNotFoundError when no taskfile is specified or found."""
    mock_find.return_value = (None, False)
    args = argparse.Namespace(agent_args=[], exec_cmd_opt=None, num_trees_opt=None, tree_indices=None, fresh_env=False, no_env_overrides=False, verbose=0)
    with pytest.raises(FileNotFoundError):
        _dispatch_exec(args)


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_with_exec_cmd_option(mock_find, mock_exec):
    """Test exec with -c option for exec_cmd."""
    mock_find.side_effect = [(Path("task.md"), False), (Path("task.md"), False)]
    args = argparse.Namespace(
        agent_args=["task.md", "3"],
        num_trees_opt=None,
        exec_cmd_opt="my-agent",
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_exec.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
    )


def test_dispatch_exec_num_trees_conflict_positional():
    """Test ValueError when num_trees is specified with -n and positionally."""
    args = argparse.Namespace(
        agent_args=["3"],
        num_trees_opt=3,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with patch("agro.cli.core.find_task_file", return_value=(None, False)):
        with pytest.raises(ValueError, match="Number of trees specified twice"):
            _dispatch_exec(args)


def test_dispatch_exec_num_trees_conflict_indices():
    """Test ValueError when num_trees is specified with -t and positionally."""
    args = argparse.Namespace(
        agent_args=["3"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices="1,2",
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with patch("agro.cli.core.find_task_file", return_value=(None, False)):
        with pytest.raises(
            ValueError,
            match="Cannot specify number of trees positionally and with -t/--tree-indices.",
        ):
            _dispatch_exec(args)
