"""Module to manage task priorities."""

from typing import List, Dict
from enum import Enum
from src.classes.errors import TaskValidationError
from src.tasks_manager.utils.query_utils import filter_by_id


class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


DEFAULT_PRIORITY = Priority.NORMAL.name


def task_priority(
    task_list, task_id: int, action: str, priority: str = None
) -> str:
    """Manage the priority of a task in the task list."""
    task = filter_by_id(tasks_list=task_list, task_id=task_id)
    if action == "set":
        return set_task_priority(task, priority)
    elif action == "get":
        return get_task_priority(task)
    elif action == "sort":
        return sort_tasks_by_priority(task_list)
    elif action == "filter":
        if not priority:
            raise TaskValidationError(
                "Priority must be provided for filtering."
            )
        return filter_tasks_by_priority(task_list, priority)
    else:
        raise TaskValidationError(
            "Invalid action. Allowed actions: set, get, sort, filter."
        )


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
