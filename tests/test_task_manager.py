# test_task_manager.py - Tests pour la logique métier
import sys
import os
import pytest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from src.task_manager import (
    get_tasks,
    create_task,
    TaskValidationError,
    _save_tasks,
    _load_tasks
)


class TestTaskManager:

    def setup_method(self):
        # Réinitialisation manuelle des données
        self.initial_tasks = [
            {
                "id": 1,
                "title": "Première tâche",
                "description": "Description de la première tâche",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00"
            },
            {
                "id": 2,
                "title": "Deuxième tâche",
                "description": "Description de la deuxième tâche",
                "status": "DONE",
                "created_at": "2024-01-02T15:00:00"
            }
        ]
        _save_tasks(self.initial_tasks)

    def test_get_tasks_returns_list(self):
        tasks = get_tasks()
        assert isinstance(tasks, list)

    def test_get_tasks_returns_two_tasks(self):
        tasks = get_tasks()
        assert len(tasks) == 2

    def test_get_tasks_returns_correct_structure(self):
        tasks = get_tasks()
        assert all(key in tasks[0] for key in ["id", "title", "description", "status", "created_at"])

    def test_create_task_with_valid_title_only(self):
        task = create_task("Nouvelle tâche")
        assert task["title"] == "Nouvelle tâche"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
        assert isinstance(datetime.fromisoformat(task["created_at"]), datetime)

    def test_create_task_with_title_and_description(self):
        task = create_task("Tâche avec description", "Une description")
        assert task["title"] == "Tâche avec description"
        assert task["description"] == "Une description"

    def test_create_task_with_title_stripped(self):
        task = create_task("   Titre entouré d'espaces   ")
        assert task["title"] == "Titre entouré d'espaces"

    def test_create_task_raises_if_title_empty(self):
        with pytest.raises(TaskValidationError, match="Title is required"):
            create_task("   ")

    def test_create_task_raises_if_title_too_long(self):
        long_title = "T" * 101
        with pytest.raises(TaskValidationError, match="Title cannot exceed 100 characters"):
            create_task(long_title)

    def test_create_task_raises_if_description_too_long(self):
        long_desc = "D" * 501
        with pytest.raises(TaskValidationError, match="Description cannot exceed 500 characters"):
            create_task("Titre valide", long_desc)

    def test_created_at_is_precise_to_second(self):
        task = create_task("Test datetime")
        now = datetime.now().replace(microsecond=0)
        created_time = datetime.fromisoformat(task["created_at"])
        assert abs((now - created_time).total_seconds()) <= 1

    def test_created_task_has_unique_id(self):
        task1 = create_task("Tâche 1")
        task2 = create_task("Tâche 2")
        assert task1["id"] != task2["id"]

    def test_task_is_persisted(self):
        task = create_task("Persistée")
        all_tasks = get_tasks()
        assert any(t["title"] == "Persistée" for t in all_tasks)