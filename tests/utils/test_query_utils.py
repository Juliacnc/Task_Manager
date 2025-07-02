import pytest


from src.tasks_manager.utils.query_utils import (
    search_tasks,
    filter_tasks_by_status,
    sorted_task,
)


class TestSearchTasks:
    def setup_method(self):
        self.tasks = [
            {
                "id": 1,
                "title": "Faire les courses",
                "description": "Acheter du lait",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            },
            {
                "id": 2,
                "title": "Appeler le docteur",
                "description": "Rendez-vous lundi",
                "status": "DONE",
                "created_at": "2024-01-02T10:00:00",
            },
            {
                "id": 3,
                "title": "Faire le ménage",
                "description": "Passer l'aspirateur",
                "status": "TODO",
                "created_at": "2024-01-03T10:00:00",
            },
            {
                "id": 4,
                "title": "Courses de Noël",
                "description": "Acheter des cadeaux",
                "status": "ONGOING",
                "created_at": "2024-01-04T10:00:00",
            },
            {
                "id": 5,
                "title": "Finir projet",
                "description": "Rendu avant la fin du mois",
                "status": "TODO",
                "created_at": "2024-01-05T10:00:00",
            },
        ]

    def test_search_by_title(self):
        expected_tasks = [self.tasks[0], self.tasks[3]]

        results = search_tasks("courses", tasks_list=self.tasks)

        # Vérifications
        assert results == expected_tasks

    def test_search_by_description(self):
        expected_tasks = [self.tasks[2]]
        results = search_tasks("aspirateur", tasks_list=self.tasks)
        assert results == expected_tasks

    def test_search_is_case_insensitive(self):
        expected_tasks = [self.tasks[1]]
        results = search_tasks("DOCTEUR", tasks_list=self.tasks)
        assert results == expected_tasks

    def test_search_empty_keyword_returns_all(self):
        results = search_tasks("", tasks_list=self.tasks)
        assert results == self.tasks

    def test_search_returns_empty_for_nonexistent_keyword(self):
        results = search_tasks("code", tasks_list=self.tasks)
        assert results == []


class TestFilterTasksByStatus:
    def setup_method(self):
        self.tasks = [
            {
                "id": 1,
                "title": "Tâche 1",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            },
            {
                "id": 2,
                "title": "Tâche 2",
                "description": "",
                "status": "DONE",
                "created_at": "2024-01-02T10:00:00",
            },
            {
                "id": 3,
                "title": "Tâche 3",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-03T10:00:00",
            },
            {
                "id": 4,
                "title": "Tâche 5",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-05T10:00:00",
            },
            {
                "id": 5,
                "title": "Tâche 6",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-06T10:00:00",
            },
        ]

    def test_filter_tasks_by_status_valid(self):
        return_value = [
            self.tasks[0],
            self.tasks[2],
            self.tasks[3],
            self.tasks[4],
        ]

        tasks = filter_tasks_by_status(status="TODO", tasks_list=self.tasks)

        assert tasks == return_value

    def test_filter_tasks_by_status_empty_result(self):
        tasks = filter_tasks_by_status(
            status="ONGOING",
            tasks_list=self.tasks,
        )

        assert tasks == []

    def test_filter_tasks_by_status_invalid_status(self):
        with pytest.raises(ValueError, match="Invalid filter status"):
            filter_tasks_by_status(
                "INVALID_STATUS", tasks_list=self.tasks, page=1, size=10
            )


class TestSortedTask:
    def setup_method(self):
        self.tasks = [
            {
                "id": 1,
                "title": "Tâche A",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            },
            {
                "id": 2,
                "title": "Tâche B",
                "description": "",
                "status": "DONE",
                "created_at": "2024-01-02T10:00:00",
            },
            {
                "id": 3,
                "title": "Tâche C",
                "description": "",
                "status": "ONGOING",
                "created_at": "2024-01-03T10:00:00",
            },
        ]

    def test_sorted_task_by_title(self):
        sorted_tasks = sorted_task(
            tasks_list=self.tasks, sort_by="title", ascending=False
        )
        assert sorted_tasks[0]["title"] == "Tâche C"
        assert sorted_tasks[1]["title"] == "Tâche B"
        assert sorted_tasks[2]["title"] == "Tâche A"

    def test_sorted_task_by_title_descending(self):
        sorted_tasks = sorted_task(
            tasks_list=self.tasks, sort_by="title", ascending=False
        )
        assert sorted_tasks[0]["title"] == "Tâche C"
        assert sorted_tasks[1]["title"] == "Tâche B"
        assert sorted_tasks[2]["title"] == "Tâche A"

    def test_sorted_task_by_created_at_descending(self):
        sorted_tasks = sorted_task(
            tasks_list=self.tasks, sort_by="created_at", ascending=False
        )
        assert sorted_tasks[0]["id"] == 3
        assert sorted_tasks[1]["id"] == 2
        assert sorted_tasks[2]["id"] == 1

    def test_sorted_task_by_status(self):
        sorted_tasks = sorted_task(tasks_list=self.tasks, sort_by="status")
        print(sorted_tasks)
        assert sorted_tasks[0]["status"] == "DONE"
        assert sorted_tasks[1]["status"] == "ONGOING"
        assert sorted_tasks[2]["status"] == "TODO"

    def test_sorted_task_invalid_sort_by(self):
        with pytest.raises(ValueError, match="Invalid sort criteria."):
            sorted_task(tasks_list=self.tasks, sort_by="invalid_field")
