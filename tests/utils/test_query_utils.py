import pytest
from src.tasks_manager.utils.query_utils import (
    search_tasks,
    filter_tasks_by_status,
    sorted_task,
    get_tasks,
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
            filter_tasks_by_status("INVALID_STATUS", tasks_list=self.tasks)


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


class TestGetTasks:
    def setup_method(self):
        self.tasks = [
            {
                "id": i,
                "title": f"Task {i}",
                "description": "",
                "status": "TODO",
                "created_at": "2024-01-01T10:00:00",
            }
            for i in range(1, 31)
        ]

    def test_get_tasks_returns_only_ten_tasks_page_one(self):
        tasks, total_tasks, total_pages = get_tasks(
            page=1, size=10, tasks_list=self.tasks
        )
        assert len(tasks) == 10
        assert total_tasks == 30
        assert total_pages == 3

    def test_get_tasks_returns_correct_page_two(self):
        tasks, total_tasks, total_pages = get_tasks(
            page=2, size=10, tasks_list=self.tasks
        )
        assert len(tasks) == 10
        assert total_tasks == 30
        assert total_pages == 3

    def test_get_tasks_should_raise_error_for_negative_page(self):
        with pytest.raises(ValueError, match="Invalid page size"):
            get_tasks(page=-1, size=10, tasks_list=self.tasks)

    def test_get_tasks_should_raise_error_for_zero_page(self):
        with pytest.raises(ValueError, match="Invalid page size"):
            get_tasks(page=0, size=10, tasks_list=self.tasks)

    def test_get_tasks_should_return_empty_list_for_too_much_page(
        self, capsys
    ):
        result = get_tasks(page=5, size=10, tasks_list=self.tasks)
        print(result)

        assert result == ([], 30, 3)
        captured = capsys.readouterr()
        assert "Page 5 n'existe pas. Total de pages: 3" in captured.out

    def test_get_tasks_should_return_empty_list_for_empty_file(self, capsys):
        tasks_list = []
        result = get_tasks(tasks_list=tasks_list)
        assert result == ([], 0, 0)
        captured = capsys.readouterr()
        assert "Total de tâches: 0" in captured.out
        assert "Total de pages: 0" in captured.out
