import pytest
from click.testing import CliRunner
from unittest.mock import patch, ANY

from src.tasks_manager.cli_tools.priority_tasks import manage_priority


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def context():
    return {"tasks_list": [{"id": 1, "title": "Tâche", "priority": "NORMAL"}]}


@patch("src.tasks_manager.cli_tools.priority_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.priority_tasks.task_priority")
def test_manage_priority_set(mock_task_priority, mock_display, runner, context):
    mock_task_priority.return_value = {"id": 1, "title": "Tâche", "priority": "HIGH"}

    result = runner.invoke(
        manage_priority,
        ["1", "set", "--priority", "HIGH"],
        obj=context,
    )

    assert result.exit_code == 0
    mock_task_priority.assert_called_once_with(ANY, 1, "set", "HIGH")
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.priority_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.priority_tasks.task_priority")
def test_manage_priority_get(mock_task_priority, mock_display, runner, context):
    mock_task_priority.return_value = {"id": 1, "title": "Tâche", "priority": "NORMAL"}

    result = runner.invoke(
        manage_priority,
        ["1", "get"],
        obj=context,
    )

    assert result.exit_code == 0
    mock_task_priority.assert_called_once_with(ANY, 1, "get", None)
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.priority_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.priority_tasks.task_priority")
def test_manage_priority_filter(mock_task_priority, mock_display, runner, context):
    mock_task_priority.return_value = {"id": 1, "title": "Tâche", "priority": "CRITICAL"}

    result = runner.invoke(
        manage_priority,
        ["1", "filter", "--priority", "CRITICAL"],
        obj=context,
    )

    assert result.exit_code == 0
    mock_task_priority.assert_called_once_with(ANY, 1, "filter", "CRITICAL")
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.priority_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.priority_tasks.task_priority")
def test_manage_priority_sort(mock_task_priority, mock_display, runner, context):
    mock_task_priority.return_value = {"id": 1, "title": "Tâche", "priority": "LOW"}

    result = runner.invoke(
        manage_priority,
        ["1", "sort"],
        obj=context,
    )

    assert result.exit_code == 0
    mock_task_priority.assert_called_once_with(ANY, 1, "sort", None)
    mock_display.assert_called_once()
