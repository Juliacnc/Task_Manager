import pytest
from src.tasks_manager.utils.task_deadline import DeadlineTask
from src.classes.errors import TaskNotFoundError


class TestDeadlineTask:
    """Test class for DeadlineTask."""

    def setup_method(self):
        """Fixture to provide a sample task list."""
        self.task = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "created_at": "2024-01-01T10:00:00",
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description 2",
                "created_at": "2024-01-02T10:00:00",
                "deadline": "2024-12-31",
            },
            {
                "id": 3,
                "title": "Task 3",
                "description": "Description 3",
                "created_at": "2024-01-03T10:00:00",
                "deadline": "2024-12-31",
            },
        ]

    def test_add_deadline_to_task(self):
        """Test adding a deadline to a task."""
        task_id = 1
        deadline = "2024-12-31"
        deadline_task = DeadlineTask(
            task_list=self.task, task_id=task_id, deadline=deadline
        )

        deadline_task.add_deadline_to_task()

        assert deadline_task.task["deadline"] == deadline

    def test_modify_task_deadline(self):
        """Test modifying the deadline of a task."""
        task_id = 2
        new_deadline = "2025-01-01"
        deadline_task = DeadlineTask(
            task_list=self.task, task_id=task_id, deadline=new_deadline
        )

        deadline_task.modify_task_deadline()
        assert deadline_task.task["deadline"] == new_deadline

    def test_remove_deadline_from_task(self):
        """Test removing the deadline from a task."""
        task_id = 3
        deadline_task = DeadlineTask(task_list=self.task, task_id=task_id)

        deadline_task.remove_deadline_from_task()
        assert deadline_task.task["deadline"] == None

    def test_invalid_task_id(self):
        """Test handling of an invalid task ID."""
        with pytest.raises(
            TaskNotFoundError, match="Task not found with ID 999."
        ):
            DeadlineTask(task_list=self.task, task_id=999)  # Non-existent ID

    def test_invalid_deadline_format(self):
        """Test handling of an invalid deadline format."""
        task_id = 1
        invalid_deadline = "31-12-2024"
        with pytest.raises(
            ValueError, match="Deadline must be in 'YYYY-MM-DD' format."
        ):
            DeadlineTask(
                task_list=self.task,
                task_id=task_id,
                deadline=invalid_deadline,
            )

    def test_past_deadline(self):
        """Test handling of a past deadline."""
        task_id = 1
        past_deadline = "2020-01-01"
        with pytest.warns(UserWarning, match="The deadline is in the past"):
            DeadlineTask(
                task_list=self.task,
                task_id=task_id,
                deadline=past_deadline,
            )
