import pytest
from click.testing import CliRunner
from unittest.mock import patch, ANY

from src.tasks_manager.cli_tools.tags import tags_cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def context():
    return {"tasks_list": [{"id": 1, "title": "Tâche", "tags": ["urgent"]}]}


@patch("src.tasks_manager.cli_tools.tags.display_tasks")
@patch("src.tasks_manager.cli_tools.tags.tags_manager")
def test_tags_add(mock_tags_manager, mock_display, runner, context):
    mock_tags_manager.return_value = (
        {"id": 1, "tags": ["urgent", "home"]},
        [{"id": 1, "title": "Tâche", "tags": ["urgent", "home"]}],
    )

    result = runner.invoke(
        tags_cli,
        ["1", "add", "home"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Task 1 updated successfully with action 'add'." in result.output
    mock_tags_manager.assert_called_once_with(ANY, 1, "add", ["home"])
    mock_display.assert_called_once()


def test_tags_add_no_tags(runner, context):
    result = runner.invoke(
        tags_cli,
        ["1", "add"],  # no tags provided
        obj=context,
    )

    assert result.exit_code == 0
    assert "No tags provided to add." in result.output


@patch("src.tasks_manager.cli_tools.tags.display_tasks")
@patch("src.tasks_manager.cli_tools.tags.tags_manager")
def test_tags_remove(mock_tags_manager, mock_display, runner, context):
    mock_tags_manager.return_value = (
        {"id": 1, "tags": []},
        [{"id": 1, "title": "Tâche", "tags": []}],
    )

    result = runner.invoke(
        tags_cli,
        ["1", "remove", "urgent"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Task 1 updated successfully with action 'remove'." in result.output
    mock_tags_manager.assert_called_once_with(ANY, 1, "remove", ["urgent"])
    mock_display.assert_called_once()


def test_tags_remove_no_tags(runner, context):
    result = runner.invoke(
        tags_cli,
        ["1", "remove"],  # no tags provided
        obj=context,
    )

    assert result.exit_code == 0
    assert "No tag provided to remove." in result.output


@patch("src.tasks_manager.cli_tools.tags.display_tasks")
@patch("src.tasks_manager.cli_tools.tags.tags_manager")
def test_tags_get_all_tags(mock_tags_manager, mock_display, runner, context):
    tags_dict = {"urgent": 3, "home": 1}
    mock_tags_manager.return_value = (tags_dict, context["tasks_list"])

    result = runner.invoke(
        tags_cli,
        ["1", "get_all_tags"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Task 1 updated successfully with action 'get_all_tags'." in result.output
    for tag, count in tags_dict.items():
        assert f"{tag}: {count}" in result.output
    mock_tags_manager.assert_called_once_with(ANY, 1, "get_all_tags", [])
    mock_display.assert_called_once()


@patch("src.tasks_manager.cli_tools.tags.display_tasks")
@patch("src.tasks_manager.cli_tools.tags.tags_manager")
def test_tags_filter(mock_tags_manager, mock_display, runner, context):
    filtered_tasks = [{"id": 1, "title": "Tâche", "tags": ["urgent"]}]
    mock_tags_manager.return_value = (filtered_tasks, filtered_tasks)

    result = runner.invoke(
        tags_cli,
        ["1", "filter", "urgent"],
        obj=context,
    )

    assert result.exit_code == 0
    assert "Task 1 updated successfully with action 'filter'." in result.output
    assert "Filtered tasks:" in result.output
    for task in filtered_tasks:
        assert f"Task ID: {task['id']}, Tags: {task.get('tags', [])}" in result.output
    mock_tags_manager.assert_called_once_with(ANY, 1, "filter", ["urgent"])
    mock_display.assert_called_once()
