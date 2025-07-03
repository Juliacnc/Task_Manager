import pytest
from src.tasks_manager.utils.task_deadline import DeadlineTask
from src.classes.errors import TaskNotFoundError


class TestDeadlineTask:
    """Test class for DeadlineTask."""

    @pytest.fixture
    def sample_task_list():
        """Fixture to provide a sample task list."""
        return [
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
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description 2",
                "created_at": "2024-01-02T10:00:00",
                "deadline": "2024-12-31",
            },
        ]

    def test_add_deadline_to_task(self, sample_task_list):
        """Test adding a deadline to a task."""
        task_id = 1
        deadline = "2024-12-31"
        deadline_task = DeadlineTask(
            task_list=sample_task_list, task_id=task_id, deadline=deadline
        )

        deadline_task.add_deadline_to_task()

        assert sample_task_list[0]["deadline"] == deadline

    def test_modify_task_deadline(self, sample_task_list):
        """Test modifying the deadline of a task."""
        task_id = 1
        new_deadline = "2025-01-01"
        deadline_task = DeadlineTask(
            task_list=sample_task_list, task_id=task_id, deadline=new_deadline
        )

        deadline_task.modify_task_deadline()
        assert sample_task_list[0]["deadline"] == new_deadline

    def test_remove_deadline_from_task(self, sample_task_list):
        """Test removing the deadline from a task."""
        task_id = 3
        deadline = "2024-12-31"
        deadline_task = DeadlineTask(
            task_list=sample_task_list, task_id=task_id, deadline=deadline
        )

        deadline_task.remove_deadline_from_task()
        assert "deadline" not in sample_task_list[0]

    def test_invalid_task_id(self, sample_task_list):
        """Test handling of an invalid task ID."""
        with pytest.raises(
            TaskNotFoundError, match="Task not found with ID 999."
        ):
            DeadlineTask(
                task_list=sample_task_list, task_id=999
            )  # Non-existent ID

    def test_invalid_deadline_format(self, sample_task_list):
        """Test handling of an invalid deadline format."""
        task_id = 1
        invalid_deadline = "31-12-2024"
        with pytest.raises(
            ValueError, match="Deadline must be in 'YYYY-MM-DD' format."
        ):
            DeadlineTask(
                task_list=sample_task_list,
                task_id=task_id,
                deadline=invalid_deadline,
            )

    def test_past_deadline(self, sample_task_list):
        """Test handling of a past deadline."""
        task_id = 1
        past_deadline = "2020-01-01"
        with pytest.raises(
            ValueError, match="Deadline cannot be in the past."
        ):
            DeadlineTask(
                task_list=sample_task_list,
                task_id=task_id,
                deadline=past_deadline,
            )
