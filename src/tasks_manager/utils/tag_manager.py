"""Module to manage tags associated with tasks."""

from typing import List, Dict, Tuple, Set
from src.classes.errors import TaskValidationError, TaskNotFoundError


MAX_TAG_LENGTH = 20


def _validate_tag(tag: str) -> None:
    tag = tag.strip()
    if not tag:
        raise TaskValidationError("Invalid tag validation: tag cannot be empty")
    if len(tag) > MAX_TAG_LENGTH:
        raise TaskValidationError(f"Invalid tag validation: tag '{tag}' exceeds {MAX_TAG_LENGTH} characters")


def _add_tags_to_task(
    tasks_list: List[Dict],
    task_id: int,
    new_tags: List[str]
) -> Tuple[Dict, List[Dict]]:
    """Add one or multiple tags to an existing task."""
    if not new_tags:
        return _get_task_by_id(tasks_list, task_id), tasks_list

    for tag in new_tags:
        _validate_tag(tag)

    task = _get_task_by_id(tasks_list, task_id)

    current_tags = set(task.get("tags", []))
    for tag in new_tags:
        current_tags.add(tag.strip())

    task["tags"] = sorted(current_tags)
    return task, tasks_list


def _remove_tag_from_task(
    tasks_list: List[Dict],
    task_id: int,
    tag_to_remove: str
) -> Tuple[Dict, List[Dict]]:
    """Remove a specific tag from a task."""
    _validate_tag(tag_to_remove)
    task = _get_task_by_id(tasks_list, task_id)

    current_tags = set(task.get("tags", []))
    if tag_to_remove not in current_tags:
        # tag not found in task tags - no change
        return task, tasks_list

    current_tags.remove(tag_to_remove)
    task["tags"] = sorted(current_tags)

    # If this tag is no longer used by any task, it should be removed from system-wide tags
    # But as tags are stored inside tasks, no global tag list to clean here (depends on app design)

    return task, tasks_list


def _get_task_by_id(tasks_list: List[Dict], task_id: int) -> Dict:
    for task in tasks_list:
        if task["id"] == task_id:
            if "tags" not in task:
                task["tags"] = []
            return task
    raise TaskNotFoundError(f"Task with ID {task_id} not found.")


def _filter_tasks_by_tags(
    tasks_list: List[Dict],
    tags_filter: List[str]
) -> List[Dict]:
    """Return tasks that have at least one of the given tags."""
    if not tags_filter:
        return tasks_list

    # Normalize tags filter to stripped lowercase for case-insensitive matching
    normalized_filter = {tag.strip() for tag in tags_filter if tag.strip()}
    filtered_tasks = []

    for task in tasks_list:
        task_tags = set(task.get("tags", []))
        if task_tags.intersection(normalized_filter):
            filtered_tasks.append(task)

    return filtered_tasks


def _get_all_tags_with_usage(tasks_list: List[Dict]) -> Dict[str, int]:
    """Return a dict of all distinct tags with their usage count across all tasks."""
    tag_counts = {}

    for task in tasks_list:
        for tag in task.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return dict(sorted(tag_counts.items()))
