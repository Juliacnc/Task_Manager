# test_task_manager.py - Tests pour la logique métier

import sys
import os
import pytest
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


from src.task_manager import (
    get_tasks,
    create_task,
    change_task_status,
    TaskValidationError,
    _save_tasks,
    get_task_by_id,
    modify_task,
    delete_task,
)


class TestTaskManager:
    def setup_method(self):
        self.initial_tasks = [
            {
                "id": 1,
                "title": "Première tâche",
                "description": "Description de la première tâche",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            },
            {
                "id": 2,
                "title": "Deuxième tâche",
                "description": "Description de la deuxième tâche",
                "status": "DONE",
                "created_at": "2024-01-02T15:00:00",
            },
        ]
        _save_tasks(self.initial_tasks)

    def test_get_task_by_id_returns_correct_task(self):
        task = get_task_by_id(1)
        assert task["id"] == 1
        assert task["title"] == "Première tâche"
        assert task["description"] == "Description de la première tâche"
        assert task["status"] == "TODO"

    def test_get_task_by_id_raises_error_for_invalid_id(self):
        with pytest.raises(
            ValueError, match="Tâche avec l'ID 999 non trouvée."
        ):
            get_task_by_id(999)

    def test_create_task_with_valid_title_only(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        task = create_task(
            "Nouvelle tâche", data_file="tests/data/test_create_task.json"
        )
        assert task["title"] == "Nouvelle tâche"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
        assert isinstance(datetime.fromisoformat(task["created_at"]), datetime)

    def test_create_task_with_title_and_description(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        task = create_task(
            "Tâche avec description",
            "Une description",
            data_file="tests/data/test_create_task.json",
        )
        assert task["title"] == "Tâche avec description"
        assert task["description"] == "Une description"

    def test_create_task_with_title_stripped(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        task = create_task(
            "   Titre entouré d'espaces   ",
            data_file="tests/data/test_create_task.json",
        )
        assert task["title"] == "Titre entouré d'espaces"

    def test_create_task_raises_if_title_empty(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        with pytest.raises(TaskValidationError, match="Title is required"):
            create_task("   ", data_file="tests/data/test_create_task.json")

    def test_create_task_raises_if_title_too_long(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError, match="Title cannot exceed 100 characters"
        ):
            create_task(
                long_title, data_file="tests/data/test_create_task.json"
            )

    def test_create_task_raises_if_description_too_long(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        long_desc = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="Description cannot exceed 500 characters",
        ):
            create_task(
                "Titre valide",
                long_desc,
                data_file="tests/data/test_create_task.json",
            )

    def test_created_at_is_precise_to_second(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        task = create_task(
            "Test datetime", data_file="tests/data/test_create_task.json"
        )
        now = datetime.now().replace(microsecond=0)
        created_time = datetime.fromisoformat(task["created_at"])
        assert abs((now - created_time).total_seconds()) <= 1

    def test_created_task_has_unique_id(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        task1 = create_task(
            "Tâche 1", data_file="tests/data/test_create_task.json"
        )
        task2 = create_task(
            "Tâche 2", data_file="tests/data/test_create_task.json"
        )
        assert task1["id"] != task2["id"]

    def test_create_task(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_create_task.json", "w")
        )
        create_task(
            "Creation tache test",
            data_file="tests/data/test_create_tasks.json",
        )

        tasks = json.load(open("tests/data/test_create_tasks.json"))

        assert any(t["title"] == "Creation tache test" for t in tasks)

    def test_modify_task_updates_title(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        modified_task = modify_task(
            1,
            title="Nouveau titre",
            data_file="tests/data/test_modify_task.json",
        )
        assert modified_task["title"] == "Nouveau titre"

    def test_modify_task_updates_description(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        modified_task = modify_task(
            1,
            description="Nouvelle description",
            data_file="tests/data/test_modify_task.json",
        )
        assert modified_task["description"] == "Nouvelle description"

    def test_modify_task_updates_with_too_long_title(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError, match="Title cannot exceed 100 characters"
        ):
            modify_task(
                1,
                title=long_title,
                data_file="tests/data/test_modify_task.json",
            )

    def test_modify_task_updates_with_too_long_description(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        long_description = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="Description cannot exceed 500 characters",
        ):
            modify_task(
                1,
                description=long_description,
                data_file="tests/data/test_modify_task.json",
            )

    def test_modify_task_raise_error_for_invalid_id(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        with pytest.raises(
            ValueError, match="Tâche avec l'ID 999 non trouvée."
        ):
            modify_task(
                999,
                title="Nouveau titre",
                data_file="tests/data/test_modify_task.json",
            )

    def test_modify_task_raises_error_for_invalid_fields(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        with pytest.raises(
            TaskValidationError,
            match="Seuls le titre et la description peuvent être modifiés.",
        ):
            modify_task(
                task_id=1,
                data_file="tests/data/test_modify_task.json",
                id=12,
                status="DONE",
                created_at="2024-01-01T10:00:00",
            )

    def test_modify_task_error_if_title_empty(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_modify_task.json", "w")
        )
        with pytest.raises(TaskValidationError, match="Title is required"):
            modify_task(
                1, title="   ", data_file="tests/data/test_modify_task.json"
            )

    def test_update_status_valid(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_update_status.json", "w")
        )
        updated = change_task_status(
            1, "ONGOING", data_file="tests/data/test_update_status.json"
        )
        tasks = json.load(open("tests/data/test_update_status.json"))
        assert updated["status"] == "ONGOING"
        assert any(t["id"] == 1 and t["status"] == "ONGOING" for t in tasks)

    def test_update_status_invalid_status(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_update_status.json", "w")
        )
        with pytest.raises(
            TaskValidationError,
            match="Invalid status. Allowed values: TODO, ONGOING, DONE",
        ):
            change_task_status(
                1, "INVALID", data_file="tests/data/test_update_status.json"
            )

    def test_update_status_nonexistent_task(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_update_status.json", "w")
        )
        with pytest.raises(Exception, match="Task not found"):
            change_task_status(
                999, "TODO", data_file="tests/data/test_update_status.json"
            )

    def test_delete_existing_task(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_delete_tasks.json", "w")
        )

        tasks_before = json.load(open("tests/data/test_delete_tasks.json"))
        delete_task(2, data_file="tests/data/test_delete_tasks.json")
        tasks_after = json.load(open("tests/data/test_delete_tasks.json"))

        assert all(t["id"] != 2 for t in tasks_after)
        assert len(tasks_after) == len(tasks_before) - 1

    def test_delete_nonexistent_task_raises(self):
        json.dump(
            self.initial_tasks, open("tests/data/test_delete_tasks.json", "w")
        )
        with pytest.raises(TaskValidationError, match="Task not found"):
            delete_task(9999, data_file="tests/data/test_delete_tasks.json")

    def test_get_tasks_returns_only_ten_tasks_page_one(self):
        tasks_list = [
            {
                "id": i,
                "title": f"Task {i}",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            }
            for i in range(1, 31)
        ]
        tasks, total_tasks, total_pages = get_tasks(
            page=1, size=10, tasks_list=tasks_list
        )
        assert len(tasks) == 10
        assert total_tasks == 30
        assert total_pages == 3

    def test_get_tasks_returns_correct_page_two(self):
        tasks_list = [
            {
                "id": i,
                "title": f"Task {i}",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            }
            for i in range(1, 31)
        ]
        tasks, total_tasks, total_pages = get_tasks(
            page=2, size=10, tasks_list=tasks_list
        )
        assert len(tasks) == 10
        assert total_tasks == 30
        assert total_pages == 3

    def test_get_tasks_should_raise_error_for_negative_page(self):
        with pytest.raises(ValueError, match="Invalid page size"):
            get_tasks(page=-1, size=10, tasks_list=self.initial_tasks)

    def test_get_tasks_should_raise_error_for_zero_page(self):
        with pytest.raises(ValueError, match="Invalid page size"):
            get_tasks(page=0, size=10, tasks_list=self.initial_tasks)

    def test_get_tasks_should_return_empty_list_for_too_much_page(
        self, capsys
    ):
        result = get_tasks(page=5, size=10, tasks_list=self.initial_tasks)
        assert result == ([], 2, 1)
        captured = capsys.readouterr()
        assert "Page 5 n'existe pas. Total de pages: 1" in captured.out

    def test_get_tasks_should_return_empty_list_for_empty_file(self, capsys):
        tasks_list = []
        result = get_tasks(tasks_list=tasks_list)
        assert result == ([], 0, 0)
        captured = capsys.readouterr()
        assert "Total de tâches: 0" in captured.out
        assert "Total de pages: 0" in captured.out
