import argparse
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
@patch("builtins.input", return_value="y")
def test_dispatch_exec_implicit_taskfile(mock_input, mock_find, mock_exec):
    """Test exec with no args, finding the latest taskfile."""
    mock_find.return_value = "path/to/latest.md"
    args = argparse.Namespace(
        agent_args=[],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with()
    mock_input.assert_called_once()
    mock_exec.assert_called_once_with(
        task_file="path/to/latest.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_explicit_taskfile(mock_find, mock_exec):
    """Test exec with an explicit taskfile."""
    mock_find.return_value = "path/to/task.md"
    args = argparse.Namespace(
        agent_args=["task.md"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_taskfile_and_num_trees(mock_find, mock_exec):
    """Test exec with taskfile and num_trees positional."""
    mock_find.return_value = "path/to/task.md"
    args = argparse.Namespace(
        agent_args=["task.md", "3"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_taskfile_and_exec_cmd(mock_find, mock_exec):
    """Test exec with taskfile and exec_cmd positional."""
    mock_find.return_value = "path/to/task.md"
    args = argparse.Namespace(
        agent_args=["task.md", "my-agent"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
    )


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_full_positional_and_agent_args(mock_find, mock_exec):
    """Test exec with taskfile, num_trees, exec_cmd, and agent args."""
    mock_find.return_value = "path/to/task.md"
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
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
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
def test_dispatch_exec_positional_swapped(mock_find, mock_exec):
    """Test exec with num_trees and exec_cmd swapped."""
    mock_find.return_value = "path/to/task.md"
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
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
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
def test_dispatch_exec_options(mock_find, mock_exec):
    """Test exec with -n, -c, and -t options."""
    mock_find.return_value = "path/to/task.md"
    args = argparse.Namespace(
        agent_args=["task.md", "--agent-opt"],
        num_trees_opt=None,
        exec_cmd_opt="my-agent",
        tree_indices="1,2",
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec.assert_called_once_with(
        task_file="path/to/task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str="1,2",
        num_trees=None,
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
    with pytest.raises(
        ValueError,
        match="Cannot specify number of trees positionally and with -t/--tree-indices.",
    ):
        _dispatch_exec(args)


@patch("agro.cli.core.find_task_file", return_value=None)
def test_dispatch_exec_explicit_taskfile_not_found(mock_find):
    """Test FileNotFoundError when explicit taskfile is not found."""
    args = argparse.Namespace(
        agent_args=["nonexistent.md"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with pytest.raises(FileNotFoundError, match="Task file 'nonexistent.md' not found"):
        _dispatch_exec(args)
