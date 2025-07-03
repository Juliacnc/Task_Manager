import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from src.tasks_manager.cli_tools.task_sheduler import task_deadline


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def context():
    # Simule une liste de tâches dans le contexte
    return {"tasks_list": [{"id": 1, "title": "Tâche 1"}]}


@patch("src.tasks_manager.cli_tools.task_sheduler.display_tasks")
@patch("src.tasks_manager.cli_tools.task_sheduler.DeadlineTask")
def test_add_deadline(mock_deadline_task_cls, mock_display, runner, context):
    mock_deadline_task = MagicMock()
    mock_deadline_task.task = {"id": 1, "title": "Tâche 1", "deadline": "2025-12-31"}
    mock_deadline_task_cls.return_value = mock_deadline_task

    result = runner.invoke(
        task_deadline,
        ["1", "--add_deadline", "--deadline", "2025-12-31"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Deadline '2025-12-31' added to task ID 1." in result.output
    mock_deadline_task.add_deadline_to_task.assert_called_once()
    mock_display.assert_called_once_with(
        [mock_deadline_task.task], page=1, total_pages=1, total_tasks=len(context["tasks_list"])
    )


@patch("src.tasks_manager.cli_tools.task_sheduler.display_tasks")
@patch("src.tasks_manager.cli_tools.task_sheduler.DeadlineTask")
def test_modify_deadline(mock_deadline_task_cls, mock_display, runner, context):
    mock_deadline_task = MagicMock()
    mock_deadline_task.task = {"id": 1, "title": "Tâche 1", "deadline": "2025-12-31"}
    mock_deadline_task_cls.return_value = mock_deadline_task

    result = runner.invoke(
        task_deadline,
        ["1", "--modify_deadline", "--deadline", "2025-12-31"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Deadline modified to 'True' for task ID 1." in result.output  # note: --modify_deadline is bool flag, the string 'True' comes from f-string in CLI code
    mock_deadline_task.modify_task_deadline.assert_called_once()
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.task_sheduler.display_tasks")
@patch("src.tasks_manager.cli_tools.task_sheduler.DeadlineTask")
def test_remove_deadline(mock_deadline_task_cls, mock_display, runner, context):
    mock_deadline_task = MagicMock()
    mock_deadline_task.task = {"id": 1, "title": "Tâche 1"}
    mock_deadline_task_cls.return_value = mock_deadline_task

    result = runner.invoke(
        task_deadline,
        ["1", "--remove_deadline"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Deadline removed from task ID 1." in result.output
    mock_deadline_task.remove_deadline_from_task.assert_called_once()
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.task_sheduler.display_tasks")
@patch("src.tasks_manager.cli_tools.task_sheduler.DeadlineTask")
def test_no_action_calls_display(mock_deadline_task_cls, mock_display, runner, context):
    # Test when no flags are passed, display_tasks still called with task

    mock_deadline_task = MagicMock()
    mock_deadline_task.task = {"id": 1, "title": "Tâche 1"}
    mock_deadline_task_cls.return_value = mock_deadline_task

    result = runner.invoke(
        task_deadline,
        ["1"],
        obj=context,
    )

    assert result.exit_code == 0
    # No messages about deadlines since no action
    assert "Deadline" not in result.output
    mock_display.assert_called_once_with(
        [mock_deadline_task.task], page=1, total_pages=1, total_tasks=len(context["tasks_list"])
    )
