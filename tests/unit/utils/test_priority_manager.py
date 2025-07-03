"""Module to test task priority management."""

import pytest
from src.tasks_manager.utils.priority_manager import (
    set_task_priority,
    get_task_priority,
    sort_tasks_by_priority,
    filter_tasks_by_priority,
)

from src.classes.errors import TaskValidationError


class TestPriorityManager:
    def setup_method(self):
        self.base_task = {"id": 1, "title": "Sample Task"}

        self.tasks = [
            {"id": 1, "title": "Tâche 1", "priority": "LOW"},
            {"id": 2, "title": "Tâche 2", "priority": "HIGH"},
            {"id": 3, "title": "Tâche 3", "priority": "CRITICAL"},
            {"id": 4, "title": "Tâche 4"},  # no priority = NORMAL
            {"id": 5, "title": "Tâche 5", "priority": "NORMAL"},
        ]

    def test_set_task_priority_valid(self):
        task = set_task_priority(self.base_task.copy(), "HIGH")
        assert task["priority"] == "HIGH"

    def test_set_task_priority_case_insensitive(self):
        task = set_task_priority(self.base_task.copy(), "low")
        assert task["priority"] == "LOW"

    def test_set_task_priority_invalid_raises(self):
        with pytest.raises(TaskValidationError, match="Invalid priority"):
            set_task_priority(self.base_task.copy(), "URGENT")

    def test_get_task_priority_default(self):
        task = self.base_task.copy()
        assert get_task_priority(task) == "NORMAL"

    def test_get_task_priority_existing(self):
        task = {"id": 2, "title": "Other Task", "priority": "CRITICAL"}
        assert get_task_priority(task) == "CRITICAL"

    def test_sort_tasks_by_priority(self):
        sorted_tasks = sort_tasks_by_priority(self.tasks)
        sorted_priorities = [get_task_priority(task) for task in sorted_tasks]
        assert sorted_priorities == ["CRITICAL", "HIGH", "NORMAL", "NORMAL", "LOW"]

    def test_filter_tasks_by_priority(self):
        filtered = filter_tasks_by_priority(self.tasks, "NORMAL")
        assert len(filtered) == 2
        assert all(get_task_priority(t) == "NORMAL" for t in filtered)

    def test_filter_tasks_invalid_priority_raises(self):
        with pytest.raises(TaskValidationError, match="Invalid priority"):
            filter_tasks_by_priority(self.tasks, "INVALID")
