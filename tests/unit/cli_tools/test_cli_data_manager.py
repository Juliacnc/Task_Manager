import pytest
from click.testing import CliRunner
from src.tasks_manager.cli_tools.cli_data_manager import (
    create_task,
    modify_task,
    change_task_status,
    delete_task,
)
from unittest.mock import patch


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def context():
    return {"tasks_list": []}


def test_create_task(runner, context):
    with patch("src.tasks_manager.cli_tools.cli_data_manager._create_task") as mock_create:
        mock_create.return_value = (
            {"id": 1, "title": "Tâche 1", "description": "Desc"},
            [{"id": 1, "title": "Tâche 1", "description": "Desc"}],
        )

        result = runner.invoke(
            create_task,
            input="Tâche 1\n",
            obj=context,
        )

        assert result.exit_code == 0
        assert "Tâche créée : Tâche 1" in result.output
        mock_create.assert_called_once_with("Tâche 1", "", [])


def test_modify_task(runner, context):
    context["tasks_list"] = [{"id": 1, "title": "Old", "description": "Old desc"}]

    with patch("src.tasks_manager.cli_tools.cli_data_manager._modify_task") as mock_modify:
        mock_modify.return_value = (
            {"id": 1, "title": "New Title", "description": "New desc"},
            [{"id": 1, "title": "New Title", "description": "New desc"}],
        )

        result = runner.invoke(
            modify_task,
            ["1", "--title", "New Title", "--description", "New desc"],
            obj=context,
        )

        assert result.exit_code == 0
        assert "Tâche modifiée : New Title" in result.output
        mock_modify.assert_called_once()


def test_change_task_status(runner, context):
    context["tasks_list"] = [{"id": 1, "title": "Tâche", "status": "todo"}]

    with patch("src.tasks_manager.cli_tools.cli_data_manager._change_task_status") as mock_status:
        mock_status.return_value = (
            {"id": 1, "status": "done"},
            [{"id": 1, "title": "Tâche", "status": "done"}],
        )

        result = runner.invoke(
            change_task_status,
            ["1", "--status", "done"],
            obj=context,
        )

        assert result.exit_code == 0
        assert "Statut de la tâche 1 changé en done" in result.output
        mock_status.assert_called_once()


def test_delete_task(runner, context):
    context["tasks_list"] = [{"id": 1, "title": "Tâche à supprimer"}]

    with patch("src.tasks_manager.cli_tools.cli_data_manager._delete_task") as mock_delete:
        mock_delete.return_value = []

        result = runner.invoke(
            delete_task,
            ["1"],
            obj=context,
        )

        assert result.exit_code == 0
        assert "Tâche avec l'ID 1 supprimée" in result.output
        mock_delete.assert_called_once_with(1, [{"id": 1, "title": "Tâche à supprimer"}])
