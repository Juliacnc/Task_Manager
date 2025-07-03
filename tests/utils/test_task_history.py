import pytest
from src.classes.errors import TaskNotFoundError, TaskValidationError
from src.tasks_manager.utils.task_history import (
    log_task_creation,
    log_task_update,
    log_status_change,
    log_assignment_change,
    log_deadline_change,
    log_priority_change,
    log_tags_change,
    get_history,
)


class TestTaskHistory:

    def setup_method(self):
        self.tasks = [
            {"id": 1, "title": "Task 1", "description": "Desc 1", "history": []},
            {"id": 2, "title": "Task 2"},
        ]

    def test_log_task_creation_adds_event(self):
        task = log_task_creation(self.tasks, 2)
        assert "history" in task
        assert task["history"][0]["event"] == "created"

    def test_log_task_update_valid(self):
        task = log_task_update(self.tasks, 1, "title", "Old", "New")
        last_event = task["history"][-1]
        assert last_event["event"] == "updated"
        assert last_event["details"]["field"] == "title"
        assert last_event["details"]["old"] == "Old"
        assert last_event["details"]["new"] == "New"

    def test_log_task_update_invalid_field(self):
        with pytest.raises(TaskValidationError):
            log_task_update(self.tasks, 1, "invalid_field", "old", "new")

    def test_log_status_change(self):
        task = log_status_change(self.tasks, 1, "todo", "done")
        last_event = task["history"][-1]
        assert last_event["event"] == "status_changed"
        assert last_event["details"]["old_status"] == "todo"
        assert last_event["details"]["new_status"] == "done"

    def test_log_assignment_change_assigned(self):
        task = log_assignment_change(self.tasks, 1, assigned_user="user1")
        last_event = task["history"][-1]
        assert last_event["event"] == "assignment_changed"
        assert last_event["details"]["assigned"] == "user1"

    def test_log_assignment_change_removed(self):
        task = log_assignment_change(self.tasks, 1, removed_user="user1")
        last_event = task["history"][-1]
        assert last_event["event"] == "assignment_changed"
        assert last_event["details"]["removed"] == "user1"

    def test_log_assignment_change_no_user_raises(self):
        with pytest.raises(TaskValidationError):
            log_assignment_change(self.tasks, 1)

    def test_log_deadline_change(self):
        task = log_deadline_change(self.tasks, 1, "2024-01-01", "2024-02-01")
        last_event = task["history"][-1]
        assert last_event["event"] == "deadline_changed"
        assert last_event["details"]["old_deadline"] == "2024-01-01"
        assert last_event["details"]["new_deadline"] == "2024-02-01"

    def test_log_priority_change(self):
        task = log_priority_change(self.tasks, 1, "low", "high")
        last_event = task["history"][-1]
        assert last_event["event"] == "priority_changed"
        assert last_event["details"]["old_priority"] == "low"
        assert last_event["details"]["new_priority"] == "high"

    def test_log_tags_change(self):
        task = log_tags_change(self.tasks, 1, ["urgent"], ["urgent", "home"])
        last_event = task["history"][-1]
        assert last_event["event"] == "tags_changed"
        assert last_event["details"]["old_tags"] == ["urgent"]
        assert last_event["details"]["new_tags"] == ["urgent", "home"]

    def test_get_history_pagination_and_order(self):
        # Add multiple events with controlled timestamps
        import datetime
        from unittest.mock import patch

        base_time = datetime.datetime(2025, 1, 1, 12, 0, 0)

        with patch('src.tasks_manager.utils.task_history.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = base_time
            mock_datetime.utcnow.isoformat = datetime.datetime.isoformat
            log_task_creation(self.tasks, 2)

            mock_datetime.utcnow.return_value = base_time + datetime.timedelta(minutes=1)
            log_status_change(self.tasks, 2, "todo", "doing")

            mock_datetime.utcnow.return_value = base_time + datetime.timedelta(minutes=2)
            log_priority_change(self.tasks, 2, "low", "high")

        history_page_1 = get_history(self.tasks, 2, page=1, per_page=2)
        assert len(history_page_1) == 2
        # The most recent event should be first
        assert history_page_1[0]["event"] == "priority_changed"
        assert history_page_1[1]["event"] == "status_changed"

    def test_task_not_found_raises(self):
        with pytest.raises(TaskNotFoundError):
            log_task_creation(self.tasks, 999)
        with pytest.raises(TaskNotFoundError):
            log_task_update(self.tasks, 999, "title", "old", "new")
        with pytest.raises(TaskNotFoundError):
            log_status_change(self.tasks, 999, "todo", "done")
        with pytest.raises(TaskNotFoundError):
            log_assignment_change(self.tasks, 999, assigned_user="user1")
        with pytest.raises(TaskNotFoundError):
            log_deadline_change(self.tasks, 999, "2024-01-01", "2024-02-01")
        with pytest.raises(TaskNotFoundError):
            log_priority_change(self.tasks, 999, "low", "high")
        with pytest.raises(TaskNotFoundError):
            log_tags_change(self.tasks, 999, [], ["tag"])
        with pytest.raises(TaskNotFoundError):
            get_history(self.tasks, 999)
