"""Module to test data manager functions in Task Manager application."""

import pytest
from datetime import datetime

from src.tasks_manager.utils.data_manager import (
    _create_task,
    _modify_task,
    _delete_task,
    _change_task_status,
)

from src.classes.errors import (
    TaskValidationError,
    TaskNotFoundError,
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

    def test_create_task_with_valid_title_only(self):
        task, _ = _create_task("Nouvelle tâche", tasks_list=self.initial_tasks)
        assert task["title"] == "Nouvelle tâche"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
        assert isinstance(datetime.fromisoformat(task["created_at"]), datetime)

    def test_create_task_with_title_and_description(self):
        task, _ = _create_task(
            "Tâche avec description",
            "Une description",
            tasks_list=self.initial_tasks,
        )
        assert task["title"] == "Tâche avec description"
        assert task["description"] == "Une description"

    def test_create_task_with_title_stripped(self):
        task, _ = _create_task(
            "   Titre entouré d'espaces   ",
            tasks_list=self.initial_tasks,
        )
        assert task["title"] == "Titre entouré d'espaces"

    def test_create_task_raises_if_title_empty(self):
        with pytest.raises(TaskValidationError, match="Title is required"):
            _create_task("   ", tasks_list=self.initial_tasks)

    def test_create_task_raises_if_title_too_long(self):
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError,
            match="Le titre ne peut pas dépasser 100 caractères",
        ):
            _create_task(long_title, tasks_list=self.initial_tasks)

    def test_create_task_raises_if_description_too_long(self):
        long_desc = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="La description ne peut pas dépasser 500 caractères",
        ):
            _create_task(
                "Titre valide",
                long_desc,
                tasks_list=self.initial_tasks,
            )

    def test_created_at_is_precise_to_second(self):
        task, _ = _create_task("Test datetime", tasks_list=self.initial_tasks)
        now = datetime.now().replace(microsecond=0)
        created_time = datetime.fromisoformat(task["created_at"])
        assert abs((now - created_time).total_seconds()) <= 1

    def test_created_task_has_unique_id(self):
        task1, tasks_list = _create_task(
            "Tâche 1", tasks_list=self.initial_tasks
        )
        task2, _ = _create_task("Tâche 2", tasks_list=tasks_list)
        assert task1["id"] != task2["id"]

    def test_create_task(self):
        _, tasks_list = _create_task(
            "Creation tache test", tasks_list=self.initial_tasks
        )
        assert any(t["title"] == "Creation tache test" for t in tasks_list)

    # --- Tests sur la US 9 : modification d'une tâche ---

    def test_modify_task_updates_title(self):
        modified_task, _ = _modify_task(
            task_id=1,
            title="Nouveau titre",
            tasks_list=self.initial_tasks,
        )
        assert modified_task["title"] == "Nouveau titre"

    def test_modify_task_updates_description(self):
        modified_task, _ = _modify_task(
            task_id=1,
            description="Nouvelle description",
            tasks_list=self.initial_tasks,
        )
        assert modified_task["description"] == "Nouvelle description"

    def test_modify_task_updates_with_too_long_title(self):
        long_title = "T" * 101
        with pytest.raises(
            TaskValidationError,
            match="Le titre ne peut pas dépasser 100 caractères",
        ):
            _modify_task(
                task_id=1,
                title=long_title,
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_updates_with_too_long_description(self):
        long_description = "D" * 501
        with pytest.raises(
            TaskValidationError,
            match="La description ne peut pas dépasser 500 caractères",
        ):
            _modify_task(
                task_id=1,
                description=long_description,
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_raise_error_for_invalid_id(self):
        with pytest.raises(
            TaskNotFoundError, match="Tâche avec l'ID 999 non trouvée."
        ):
            _modify_task(
                task_id=999,
                title="Nouveau titre",
                tasks_list=self.initial_tasks,
            )

    def test_modify_task_raises_error_for_invalid_fields(self):
        with pytest.raises(
            TaskValidationError,
            match="Seuls le titre et la description peuvent être modifiés.",
        ):
            _modify_task(
                task_id=1,
                tasks_list=self.initial_tasks,
                id=12,
                status="DONE",
                created_at="2024-01-01T10:00:00",
            )

    def test_modify_task_error_if_title_empty(self):
        with pytest.raises(
            TaskValidationError, match="Le titre est obligatoire"
        ):
            _modify_task(task_id=1, title="   ", tasks_list=self.initial_tasks)

    def test_delete_existing_task(self):
        tasks_before = self.initial_tasks.copy()
        tasks_after = _delete_task(2, self.initial_tasks.copy())

        assert all(t["id"] != 2 for t in tasks_after)
        assert len(tasks_after) == len(tasks_before) - 1

    def test_delete_nonexistent_task_raises(self):
        with pytest.raises(
            TaskNotFoundError, match="Tâche avec l'ID 9999 non trouvée."
        ):
            _delete_task(
                tasks_list=self.initial_tasks,
                task_id=9999,
            )

    def test_update_status_valid(self):
        updated, tasks = _change_task_status(
            tasks_list=self.initial_tasks,
            task_id=1,
            new_status="ONGOING",
        )
        assert updated["status"] == "ONGOING"
        assert any(t["id"] == 1 and t["status"] == "ONGOING" for t in tasks)

    def test_update_status_invalid_status(self):
        with pytest.raises(
            TaskValidationError,
            match="Statut invalide. Valeurs autorisées : TODO, ONGOING, DONE",
        ):
            _change_task_status(
                tasks_list=self.initial_tasks, task_id=1, new_status="INVALID"
            )

    def test_update_status_nonexistent_task(self):
        with pytest.raises(
            Exception, match="Tâche avec l'ID 999 non trouvée."
        ):
            _change_task_status(
                tasks_list=self.initial_tasks, task_id=999, new_status="TODO"
            )
