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
    list_tasks_paginated,
    search_tasks,
    filter_tasks_by_status,
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

    def test_get_tasks_returns_list(self):
        tasks = get_tasks()
        assert isinstance(tasks, list)

    def test_get_tasks_returns_two_tasks(self):
        tasks = get_tasks()
        assert len(tasks) == 2

    def test_get_tasks_returns_correct_structure(self):
        tasks = get_tasks()
        assert "id" in tasks[0]
        assert "title" in tasks[0]
        assert "description" in tasks[0]
        assert "status" in tasks[0]

    def test_get_task_by_id_returns_correct_task(self):
        task = get_task_by_id(1)
        assert task["id"] == 1
        assert task["title"] == "Première tâche"
        assert task["description"] == "Description de la première tâche"
        assert task["status"] == "TODO"

    def test_get_task_by_id_raises_error_for_invalid_id(self):
        with pytest.raises(ValueError, match="Tâche avec l'ID 999 non trouvée."):
            get_task_by_id(999)

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

    def test_modify_task_updates_title(self):
        task = create_task("Tâche à modifier")
        modified_task = modify_task(task["id"], title="Nouveau titre")
        assert modified_task["title"] == "Nouveau titre"

    def test_modify_task_updates_description(self):
        task = create_task("Tâche à modifier")
        modified_task = modify_task(task["id"], description="Nouvelle description")
        assert modified_task["description"] == "Nouvelle description"

    def test_modify_task_updates_with_too_long_title(self):
        task = create_task("Tâche à modifier")
        long_title = "T" * 101
        with pytest.raises(TaskValidationError, match="Title cannot exceed 100 characters"):
            modify_task(task["id"], title=long_title)

    def test_modify_task_updates_with_too_long_description(self):
        task = create_task("Tâche à modifier")
        long_description = "D" * 501
        with pytest.raises(TaskValidationError, match="Description cannot exceed 500 characters"):
            modify_task(task["id"], description=long_description)

    def test_modify_task_raise_error_for_invalid_id(self):
        with pytest.raises(ValueError, match="Tâche avec l'ID 999 non trouvée."):
            modify_task(999, title="Nouveau titre")

    def test_modify_task_raises_error_for_invalid_fields(self):
        task = create_task("Tâche à modifier")
        with pytest.raises(TaskValidationError, match="Seuls le titre et la description peuvent être modifiés."):
            modify_task(task["id"], id=12, status="DONE", created_at="2024-01-01T10:00:00")

    def test_modify_task_error_if_title_empty(self):
        task = create_task("Tâche à modifier")
        with pytest.raises(TaskValidationError, match="Title is required"):
            modify_task(task["id"], title="   ")

    def test_update_status_valid(self):
        updated = change_task_status(1, "ONGOING")
        assert updated["status"] == "ONGOING"
        tasks = get_tasks()
        assert any(t["id"] == 1 and t["status"] == "ONGOING" for t in tasks)

    def test_update_status_invalid_status(self):
        with pytest.raises(TaskValidationError, match="Invalid status. Allowed values: TODO, ONGOING, DONE"):
            change_task_status(1, "INVALID")

    def test_update_status_nonexistent_task(self):
        with pytest.raises(Exception, match="Task not found"):
            change_task_status(999, "TODO")

    def test_delete_existing_task(self):
        task = create_task("Tâche temporaire")
        task_id = task["id"]
        tasks_before = get_tasks()

        delete_task(task_id)
        tasks_after = get_tasks()

        assert all(t["id"] != task_id for t in tasks_after)
        assert len(tasks_after) == len(tasks_before) - 1

    def test_delete_nonexistent_task_raises(self):
        with pytest.raises(TaskValidationError, match="Task not found"):
            delete_task(9999)

    def test_pagination_returns_correct_number_of_tasks(self):
        for i in range(25):
            create_task(f"Tâche {i+1}")

        result = list_tasks_paginated(page=1, size=10)
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert result["total_items"] >= 25
        assert len(result["tasks"]) == 10

    def test_pagination_returns_empty_if_page_too_high(self):
        result = list_tasks_paginated(page=100, size=10)
        assert result["tasks"] == []

    def test_pagination_default_to_20(self):
        for i in range(30):
            create_task(f"Tâche test {i}")
        result = list_tasks_paginated()
        assert result["page_size"] == 20
        assert len(result["tasks"]) == 20

    def test_invalid_page_size_raises_error(self):
        with pytest.raises(TaskValidationError, match="Invalid page size"):
            list_tasks_paginated(size=0)

    def test_search_by_keyword_in_title(self):
        create_task("Acheter du pain")
        result = search_tasks("pain")
        assert any("pain" in t["title"].lower() for t in result["tasks"])

    def test_search_by_keyword_in_description(self):
        create_task("Titre générique", "Aller à la boulangerie")
        result = search_tasks("boulangerie")
        assert any("boulangerie" in t["description"].lower() for t in result["tasks"])

    def test_search_is_case_insensitive(self):
        create_task("Nettoyer la voiture")
        result = search_tasks("VOITURE")
        assert len(result["tasks"]) > 0

    def test_search_with_empty_keyword_returns_all(self):
        result_all = search_tasks("")
        result_get_tasks = get_tasks()
        assert len(result_all["tasks"]) == len(result_get_tasks)

    def test_filter_by_valid_status(self):
        create_task("Tâche TODO")
        t2 = create_task("Tâche DONE")
        change_task_status(t2["id"], "DONE")

        result = filter_tasks_by_status("DONE")
        assert all(t["status"] == "DONE" for t in result["tasks"])

    def test_filter_by_invalid_status_raises(self):
        with pytest.raises(TaskValidationError, match="Invalid filter status"):
            filter_tasks_by_status("FINISHED")

    def test_filter_by_status_with_no_match_returns_empty(self):
        result = filter_tasks_by_status("ONGOING")
        assert isinstance(result["tasks"], list)
