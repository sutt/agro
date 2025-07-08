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


def test_dispatch_exec_simple():
    """Test exec with just a taskfile."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=[],
        num_trees_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            no_all_extras=False,
            agent_args=[],
            exec_cmd=None,
            indices_str=None,
            num_trees=None,
            show_cmd_output=False,
        )


def test_dispatch_exec_with_num_trees_positional():
    """Test exec with taskfile and num_trees positional arg."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["3"],
        num_trees_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            no_all_extras=False,
            agent_args=[],
            exec_cmd=None,
            indices_str=None,
            num_trees=3,
            show_cmd_output=False,
        )


def test_dispatch_exec_with_exec_cmd_positional():
    """Test exec with taskfile and exec_cmd positional arg."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["my-agent"],
        num_trees_opt=None,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            no_all_extras=False,
            agent_args=[],
            exec_cmd="my-agent",
            indices_str=None,
            num_trees=None,
            show_cmd_output=False,
        )


def test_dispatch_exec_with_num_trees_and_exec_cmd_positional():
    """Test exec with taskfile, num_trees, and exec_cmd positional args."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["3", "my-agent", "--agent-opt"],
        num_trees_opt=None,
        tree_indices=None,
        fresh_env=True,
        no_env_overrides=True,
        no_all_extras=True,
        verbose=2,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=True,
            no_overrides=True,
            no_all_extras=True,
            agent_args=["--agent-opt"],
            exec_cmd="my-agent",
            indices_str=None,
            num_trees=3,
            show_cmd_output=True,
        )


def test_dispatch_exec_with_num_trees_option():
    """Test exec with -n option for num_trees."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["my-agent", "--agent-opt"],
        num_trees_opt=3,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            no_all_extras=False,
            agent_args=["--agent-opt"],
            exec_cmd="my-agent",
            indices_str=None,
            num_trees=3,
            show_cmd_output=False,
        )


def test_dispatch_exec_with_tree_indices_option():
    """Test exec with -t option for tree_indices."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["my-agent", "--agent-opt"],
        num_trees_opt=None,
        tree_indices="1,2,3",
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with patch("agro.cli.core.exec_agent") as mock_exec_agent:
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            no_all_extras=False,
            agent_args=["--agent-opt"],
            exec_cmd="my-agent",
            indices_str="1,2,3",
            num_trees=None,
            show_cmd_output=False,
        )


def test_dispatch_exec_num_trees_conflict_positional():
    """Test ValueError when num_trees is specified with -n and positionally."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["3"],
        num_trees_opt=3,
        tree_indices=None,
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with pytest.raises(ValueError, match="Number of trees specified twice"):
        _dispatch_exec(args)


def test_dispatch_exec_num_trees_conflict_indices():
    """Test ValueError when num_trees is specified with -t and positionally."""
    args = argparse.Namespace(
        taskfile="task.md",
        agent_args=["3"],
        num_trees_opt=None,
        tree_indices="1,2",
        fresh_env=False,
        no_env_overrides=False,
        no_all_extras=False,
        verbose=0,
    )
    with pytest.raises(
        ValueError,
        match="Cannot specify number of trees positionally and with -t/--tree-indices.",
    ):
        _dispatch_exec(args)
