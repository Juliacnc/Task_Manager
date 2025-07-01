# test_task_manager.py - Tests pour la logique métier

import sys
import os
import pytest
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
    search_tasks,
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
        task = get_task_by_id(1, tasks_list=self.initial_tasks)
        assert task["id"] == 1
        assert task["title"] == "Première tâche"
        assert task["description"] == "Description de la première tâche"
        assert task["status"] == "TODO"

    def test_get_task_by_id_raises_error_for_invalid_id(self):
        with pytest.raises(
            ValueError, match="Tâche avec l'ID 999 non trouvée."
        ):
            get_task_by_id(999, tasks_list=self.initial_tasks)

    def test_create_task_with_valid_title_only(self):
        task, _ = create_task("Nouvelle tâche", tasks_list=self.initial_tasks)
        assert task["title"] == "Nouvelle tâche"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
        assert isinstance(datetime.fromisoformat(task["created_at"]), datetime)

    def test_create_task_with_title_and_description(self):
        task, _ = create_task(
            "Tâche avec description",
            "Une description",
            tasks_list=self.initial_tasks,
        )
        assert task["title"] == "Tâche avec description"
        assert task["description"] == "Une description"

    def test_create_task_with_title_stripped(self):
        task, _ = create_task(
            "   Titre entouré d'espaces   ",
            tasks_list=self.initial_tasks,
        )
        assert task["title"] == "Titre entouré d'espaces"

    def test_create_task_raises_if_title_empty(self):
        with pytest.raises(TaskValidationError, match="Title is required"):
            create_task("   ", tasks_list=self.initial_tasks)

    def test_create_task_raises_if_title_too_long(self):
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError, match="Title cannot exceed 100 characters"
        ):
            create_task(long_title, tasks_list=self.initial_tasks)

    def test_create_task_raises_if_description_too_long(self):
        long_desc = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="Description cannot exceed 500 characters",
        ):
            create_task(
                "Titre valide",
                long_desc,
                tasks_list=self.initial_tasks,
            )

    def test_created_at_is_precise_to_second(self):
        task, _ = create_task("Test datetime", tasks_list=self.initial_tasks)
        now = datetime.now().replace(microsecond=0)
        created_time = datetime.fromisoformat(task["created_at"])
        assert abs((now - created_time).total_seconds()) <= 1

    def test_created_task_has_unique_id(self):
        task1, tasks_list = create_task(
            "Tâche 1", tasks_list=self.initial_tasks
        )
        task2, _ = create_task("Tâche 2", tasks_list=tasks_list)
        assert task1["id"] != task2["id"]

    def test_create_task(self):
        _, tasks_list = create_task(
            "Creation tache test", tasks_list=self.initial_tasks
        )

        assert any(t["title"] == "Creation tache test" for t in tasks_list)

    def test_modify_task_updates_title(self):
        modified_task, _ = modify_task(
            task_id=1,
            title="Nouveau titre",
            tasks_list=self.initial_tasks,
        )
        assert modified_task["title"] == "Nouveau titre"

    def test_modify_task_updates_description(self):
        modified_task, _ = modify_task(
            task_id=1,
            description="Nouvelle description",
            tasks_list=self.initial_tasks,
        )
        assert modified_task["description"] == "Nouvelle description"

    def test_modify_task_updates_with_too_long_title(self):
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError, match="Title cannot exceed 100 characters"
        ):
            modify_task(
                task_id=1,
                title=long_title,
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_updates_with_too_long_description(self):
        long_description = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="Description cannot exceed 500 characters",
        ):
            modify_task(
                task_id=1,
                description=long_description,
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_raise_error_for_invalid_id(self):
        with pytest.raises(
            ValueError, match="Tâche avec l'ID 999 non trouvée."
        ):
            modify_task(
                task_id=999,
                title="Nouveau titre",
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_raises_error_for_invalid_fields(self):
        with pytest.raises(
            TaskValidationError,
            match="Seuls le titre et la description peuvent être modifiés.",
        ):
            modify_task(
                task_id=1,
                tasks_list=self.initial_tasks,
                id=12,
                status="DONE",
                created_at="2024-01-01T10:00:00",
            )

    def test_modify_task_error_if_title_empty(self):
        with pytest.raises(TaskValidationError, match="Title is required"):
            modify_task(task_id=1, title="   ", tasks_list=self.initial_tasks)

    def test_update_status_valid(self):
        updated, tasks = change_task_status(
            1, "ONGOING", tasks_list=self.initial_tasks
        )
        assert updated["status"] == "ONGOING"
        assert any(t["id"] == 1 and t["status"] == "ONGOING" for t in tasks)

    def test_update_status_invalid_status(self):
        with pytest.raises(
            TaskValidationError,
            match="Invalid status. Allowed values: TODO, ONGOING, DONE",
        ):
            change_task_status(1, "INVALID", tasks_list=self.initial_tasks)

    def test_update_status_nonexistent_task(self):
        with pytest.raises(Exception, match="Task not found"):
            change_task_status(999, "TODO", tasks_list=self.initial_tasks)

    def test_delete_existing_task(self):
        tasks_before = self.initial_tasks.copy()
        tasks_after = delete_task(2, self.initial_tasks.copy())

        assert all(t["id"] != 2 for t in tasks_after)
        assert len(tasks_after) == len(tasks_before) - 1

    def test_delete_nonexistent_task_raises(self):
        with pytest.raises(TaskValidationError, match="Task not found"):
            delete_task(9999, tasks_list=self.initial_tasks)

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


    class TestSearchTasks:
    def setup_method(self):
        self.tasks = [
            {"id": 1, "title": "Faire les courses", "description": "Acheter du lait", "status": "TODO", "created_at": "2024-01-01T10:00:00"},
            {"id": 2, "title": "Appeler le docteur", "description": "Rendez-vous lundi", "status": "DONE", "created_at": "2024-01-02T10:00:00"},
            {"id": 3, "title": "Faire le ménage", "description": "Passer l'aspirateur", "status": "TODO", "created_at": "2024-01-03T10:00:00"},
            {"id": 4, "title": "Courses de Noël", "description": "Acheter des cadeaux", "status": "ONGOING", "created_at": "2024-01-04T10:00:00"},
            {"id": 5, "title": "Finir projet", "description": "Rendu avant la fin du mois", "status": "TODO", "created_at": "2024-01-05T10:00:00"},
        ]
        _save_tasks(self.tasks, data_file="tests/data/test_search_tasks.json")

    def test_search_by_title(self):
        results, total, pages = search_tasks("courses", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 2
        assert any(task["id"] == 1 for task in results)
        assert any(task["id"] == 4 for task in results)

    def test_search_by_description(self):
        results, total, pages = search_tasks("aspirateur", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 1
        assert results[0]["id"] == 3

    def test_search_is_case_insensitive(self):
        results, total, pages = search_tasks("DOCTEUR", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 1
        assert results[0]["id"] == 2

    def test_search_empty_keyword_returns_all(self):
        results, total, pages = search_tasks("", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == len(self.tasks)
        assert len(results) == len(self.tasks)

    def test_search_pagination(self):
        results, total, pages = search_tasks("t", page=1, size=2, data_file="tests/data/test_search_tasks.json")
        assert total >= 2
        assert len(results) <= 2
        results2, _, _ = search_tasks("t", page=2, size=2, data_file="tests/data/test_search_tasks.json")
        assert results != results2

    def test_search_page_out_of_bounds_returns_empty(self):
        results, total, pages = search_tasks("courses", page=10, size=2, data_file="tests/data/test_search_tasks.json")
        assert results == []
class TestSearchTasks:
    def setup_method(self):
        self.tasks = [
            {"id": 1, "title": "Faire les courses", "description": "Acheter du lait", "status": "TODO", "created_at": "2024-01-01T10:00:00"},
            {"id": 2, "title": "Appeler le docteur", "description": "Rendez-vous lundi", "status": "DONE", "created_at": "2024-01-02T10:00:00"},
            {"id": 3, "title": "Faire le ménage", "description": "Passer l'aspirateur", "status": "TODO", "created_at": "2024-01-03T10:00:00"},
            {"id": 4, "title": "Courses de Noël", "description": "Acheter des cadeaux", "status": "ONGOING", "created_at": "2024-01-04T10:00:00"},
            {"id": 5, "title": "Finir projet", "description": "Rendu avant la fin du mois", "status": "TODO", "created_at": "2024-01-05T10:00:00"},
        ]
        _save_tasks(self.tasks, data_file="tests/data/test_search_tasks.json")

    def test_search_by_title(self):
        results, total, pages = search_tasks("courses", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 2
        assert any(task["id"] == 1 for task in results)
        assert any(task["id"] == 4 for task in results)

    def test_search_by_description(self):
        results, total, pages = search_tasks("aspirateur", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 1
        assert results[0]["id"] == 3

    def test_search_is_case_insensitive(self):
        results, total, pages = search_tasks("DOCTEUR", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == 1
        assert results[0]["id"] == 2

    def test_search_empty_keyword_returns_all(self):
        results, total, pages = search_tasks("", page=1, size=10, data_file="tests/data/test_search_tasks.json")
        assert total == len(self.tasks)
        assert len(results) == len(self.tasks)

    def test_search_pagination(self):
        results, total, pages = search_tasks("t", page=1, size=2, data_file="tests/data/test_search_tasks.json")
        assert total >= 2
        assert len(results) <= 2
        results2, _, _ = search_tasks("t", page=2, size=2, data_file="tests/data/test_search_tasks.json")
        assert results != results2

    def test_search_page_out_of_bounds_returns_empty(self):
        results, total, pages = search_tasks("courses", page=10, size=2, data_file="tests/data/test_search_tasks.json")
        assert results == []
