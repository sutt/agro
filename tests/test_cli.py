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


from pathlib import Path


@patch("agro.cli.core.exec_agent")
@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
@patch("agro.cli.core.find_task_file")
def test_dispatch_exec_simple(mock_find, mock_find_recent, mock_exec_agent):
    """Test exec with just a taskfile."""
    mock_find.return_value = Path("task.md")
    args = argparse.Namespace(
        agent_args=["task.md"],
        num_trees_opt=None,
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_find.assert_called_once_with("task.md")
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_find.assert_any_call("task.md")
    mock_find.assert_any_call("my-agent")
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=True,
        no_env_overrides=True,
        verbose=2,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=True,
        no_overrides=True,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=True,
        agent_type=None,
        auto_commit=True,
    )


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=True,
        no_env_overrides=True,
        verbose=2,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=True,
        no_overrides=True,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=True,
        agent_type=None,
        auto_commit=True,
    )


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=3,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )



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
        exec_cmd_opt="my-agent",
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=["--agent-opt"],
        exec_cmd="my-agent",
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )


def test_dispatch_exec_num_trees_conflict_positional():
    """Test ValueError when num_trees is specified with -n and positionally."""
    args = argparse.Namespace(
        agent_args=["3"],
        num_trees_opt=3,
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with pytest.raises(ValueError, match="Number of trees specified twice"):
        _dispatch_exec(args)



def test_dispatch_exec_exec_cmd_conflict():
    """Test ValueError when exec_cmd is specified with -c and positionally."""
    args = argparse.Namespace(
        agent_args=["my-agent"],
        num_trees_opt=None,
        exec_cmd_opt="my-agent",
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with patch("agro.cli.core.find_task_file", return_value=None):
        with pytest.raises(ValueError, match="Cannot specify exec-cmd twice."):
            _dispatch_exec(args)


@patch("agro.cli.core.find_task_file", return_value=None)
@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
def test_dispatch_exec_no_taskfile_found(mock_find_recent, mock_find):
    """Test FileNotFoundError when no taskfile is found."""
    args = argparse.Namespace(
        agent_args=[],
        num_trees_opt=None,
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    with pytest.raises(FileNotFoundError):
        _dispatch_exec(args)


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
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_input.assert_called_once()
    mock_exec_agent.assert_called_once_with(
        task_file="recent.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd=None,
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
        agent_type=None,
        auto_commit=True,
    )


@patch("agro.cli.core.exec_agent")
@patch("builtins.input", return_value="n")
@patch("agro.cli.core.find_most_recent_task_file", return_value=Path("recent.md"))
@patch("agro.cli.core.find_task_file", return_value=None)
def test_dispatch_exec_no_taskfile_use_recent_confirm_no(
    mock_find, mock_find_recent, mock_input, mock_exec_agent
):
    """Test cancelling when user does not confirm recent taskfile."""
    args = argparse.Namespace(
        agent_args=[],
        num_trees_opt=None,
        exec_cmd_opt=None,
        agent_type_opt=None,
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
    )
    _dispatch_exec(args)
    mock_input.assert_called_once()
    mock_exec_agent.assert_not_called()


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
        exec_cmd_opt=None,
        agent_type_opt="gemini",
        fresh_env=False,
        no_env_overrides=False,
        verbose=0,
        no_auto_commit=False,
    )
    _dispatch_exec(args)
    mock_exec_agent.assert_called_once_with(
        task_file="task.md",
        fresh_env=False,
        no_overrides=False,
        agent_args=[],
        exec_cmd="gemini",
        indices_str=None,
        num_trees=None,
        show_cmd_output=False,
        agent_type="gemini",
        auto_commit=True,
    )


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
            exec_cmd_opt="my-gemini-agent",
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
            no_auto_commit=False,
        )
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            agent_args=[],
            exec_cmd="my-gemini-agent",
            indices_str=None,
            num_trees=None,
            show_cmd_output=False,
            agent_type="gemini",
            auto_commit=True,
        )


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
            exec_cmd_opt=None,
            agent_type_opt=None,
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
            no_auto_commit=False,
        )
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            agent_args=[],
            exec_cmd="my-gemini-agent",
            indices_str=None,
            num_trees=None,
            show_cmd_output=False,
            agent_type="gemini",
            auto_commit=True,
        )


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
            exec_cmd_opt="my-gemini-agent",
            agent_type_opt="aider",
            fresh_env=False,
            no_env_overrides=False,
            verbose=0,
            no_auto_commit=False,
        )
        _dispatch_exec(args)
        mock_exec_agent.assert_called_once_with(
            task_file="task.md",
            fresh_env=False,
            no_overrides=False,
            agent_args=[],
            exec_cmd="my-gemini-agent",
            indices_str=None,
            num_trees=None,
            show_cmd_output=False,
            agent_type="aider",
            auto_commit=True,
        )
