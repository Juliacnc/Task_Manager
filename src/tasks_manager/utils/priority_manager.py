"""Module to manage task priorities."""

from typing import List, Dict
from enum import Enum
from src.classes.errors import TaskValidationError


class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


DEFAULT_PRIORITY = Priority.NORMAL.name


def set_task_priority(task: Dict, priority: str) -> Dict:
    """Assigns a priority to a task."""
    priority = priority.upper()
    if priority not in Priority.__members__:
        raise TaskValidationError(
            "Invalid priority. Allowed values: LOW, NORMAL, HIGH, CRITICAL"
        )
    task["priority"] = priority
    return task


def get_task_priority(task: Dict) -> str:
    """Returns the priority of a task, defaulting to NORMAL if not set."""
    return task.get("priority", DEFAULT_PRIORITY)


def sort_tasks_by_priority(tasks: List[Dict]) -> List[Dict]:
    """Sorts tasks by priority from highest to lowest."""
    def get_priority_value(task: Dict) -> int:
        return Priority[get_task_priority(task)].value

    return sorted(tasks, key=get_priority_value, reverse=True)


def filter_tasks_by_priority(tasks: List[Dict], priority: str) -> List[Dict]:
    """Returns only tasks that match a given priority."""
    priority = priority.upper()
    if priority not in Priority.__members__:
        raise TaskValidationError(
            "Invalid priority. Allowed values: LOW, NORMAL, HIGH, CRITICAL"
        )
    return [task for task in tasks if get_task_priority(task) == priority]
