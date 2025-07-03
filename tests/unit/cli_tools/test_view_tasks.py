import pytest
from click.testing import CliRunner
from unittest.mock import patch
from src.tasks_manager.cli_tools.view_tasks import view_tasks


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def context():
    # Ajout de "created_at" car le tri par défaut utilise cette clé
    return {
        "tasks_list": [
            {"id": 1, "title": "Task 1", "status": "TODO", "created_at": "2023-01-01T00:00:00"}
        ]
    }


@patch("src.tasks_manager.cli_tools.view_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.view_tasks.get_tasks")
@patch("src.tasks_manager.cli_tools.view_tasks.sorted_task")
@patch("src.tasks_manager.cli_tools.view_tasks.search_tasks")
@patch("src.tasks_manager.cli_tools.view_tasks.filter_tasks_by_status")
@patch("src.tasks_manager.cli_tools.view_tasks.filter_by_id")
def test_view_tasks_all_filters(
    mock_filter_by_id,
    mock_filter_by_status,
    mock_search_tasks,
    mock_sorted_task,
    mock_get_tasks,
    mock_display,
    runner,
    context,
):
    # Setup mocks
    mock_filter_by_id.return_value = {"id": 1, "title": "Task 1", "status": "TODO", "created_at": "2023-01-01T00:00:00"}
    mock_filter_by_status.return_value = [mock_filter_by_id.return_value]
    mock_search_tasks.return_value = [mock_filter_by_status.return_value[0]]
    mock_sorted_task.return_value = [mock_search_tasks.return_value[0]]
    mock_get_tasks.return_value = (mock_sorted_task.return_value, 1, 1)

    result = runner.invoke(
        view_tasks,
        [
            "--id",
            "1",
            "--status",
            "TODO",
            "--search",
            "Task",
            "--sort_by",
            "title",
            "--asc",
            "--page",
            "1",
            "--size",
            "10",
        ],
        obj=context,
    )

    assert result.exit_code == 0

    # Vérifie que chaque fonction a été appelée correctement
    mock_filter_by_id.assert_called_once_with(1, context["tasks_list"])
    mock_filter_by_status.assert_called_once_with("TODO", [mock_filter_by_id.return_value])
    mock_search_tasks.assert_called_once_with("Task", mock_filter_by_status.return_value)
    mock_sorted_task.assert_called_once_with(mock_search_tasks.return_value, sort_by="title", ascending=True)
    mock_get_tasks.assert_called_once_with(1, 10, mock_sorted_task.return_value)

    mock_display.assert_called_once_with(mock_get_tasks.return_value[0], 1, 1, 1)


@patch("src.tasks_manager.cli_tools.view_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.view_tasks.get_tasks")
def test_view_tasks_no_filters(mock_get_tasks, mock_display, runner, context):
    mock_get_tasks.return_value = (context["tasks_list"], 1, 1)

    result = runner.invoke(view_tasks, [], obj=context)

    assert result.exit_code == 0
    mock_get_tasks.assert_called_once_with(1, 10, context["tasks_list"])
    mock_display.assert_called_once_with(context["tasks_list"], 1, 1, 1)


@patch("src.tasks_manager.cli_tools.view_tasks.display_tasks")
@patch("src.tasks_manager.cli_tools.view_tasks.filter_by_id")
def test_view_tasks_id_not_found(mock_filter_by_id, mock_display, runner, context):
    mock_filter_by_id.return_value = None

    result = runner.invoke(view_tasks, ["--id", "999"], obj=context)

    assert result.exit_code == 0
    # Quand id introuvable, tasks_list devient vide, display_tasks appelé avec []
    mock_display.assert_called_once_with([], 1, 0, 0)
