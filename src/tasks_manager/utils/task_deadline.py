from datetime import datetime
import warnings
from src.classes.errors import TaskNotFoundError


class DeadlineTask:
    def __init__(self, task_list, task_id, deadline=None):
        """Initializes the DeadlineTask"""
        self.task_list = task_list
        self.task_id = task_id
        self.deadline = deadline
        self.task = next(
            (task for task in task_list if task["id"] == task_id), None
        )

        # check if the task exists
        if self.task is None:
            raise TaskNotFoundError(f"Task not found with ID {task_id}.")

        # check if the deadline is in the correct format
        if self.deadline:
            try:
                datetime.strptime(self.deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Deadline must be in 'YYYY-MM-DD' format.")

        # check if the deadline is not in the past
        if self.deadline:
            deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d")
            if deadline_date < datetime.now():
                warnings.warn(
                    "The deadline is in the past",
                    UserWarning,
                )

    def _update(self):
        """Updates the task in the task list."""
        for i, task in enumerate(self.task_list):
            if task["id"] == self.task_id:
                self.task_list[i] = self.task
                break

    def add_deadline_to_task(self):
        """Adds a deadline to a task.

        Args:
            task (dict): The task to which the deadline will be added.
            deadline (str): The deadline to be added in 'YYYY-MM-DD' format.

        Returns:
            dict: The updated task with the deadline added.
        """
        self.task["deadline"] = self.deadline
        print(f"Adding deadline {self.deadline} to task {self.task}")

        self._update()

    def modify_task_deadline(self):
        """Modifies the deadline of a task.

        Args:
            task (dict): The task whose deadline will be modified.
            new_deadline (str): The new deadline in 'YYYY-MM-DD' format.

        Returns:
            dict: The updated task with the modified deadline.
        """
        if "deadline" in self.task:
            self.task["deadline"] = self.deadline
        else:
            raise KeyError("Task does not have a deadline to modify.")
        self._update()

    def remove_deadline_from_task(self):
        """Removes the deadline from a task.

        Args:
            task (dict): The task from which the deadline will be removed.

        Returns:
            dict: The updated task without the deadline.
        """
        if "deadline" in self.task:
            self.task["deadline"] = None
        else:
            raise KeyError("Task does not have a deadline to remove.")
        self._update()
