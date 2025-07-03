from datetime import datetime
from src.classes.errors import TaskNotFoundError, TaskValidationError


def _get_task_by_id(tasks, task_id):
    for task in tasks:
        if task.get("id") == task_id:
            return task
    raise TaskNotFoundError(f"Task with id {task_id} not found")


def _init_history(task):
    if "history" not in task:
        task["history"] = []
        task["history"].append({
            "event": "created",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "details": {"title": task.get("title", ""), "description": task.get("description", "")}
        })


def _add_history_event(task, event_type, details):
    if "history" not in task:
        _init_history(task)
    task["history"].append({
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "details": details
    })


def log_task_creation(tasks, task_id):
    task = _get_task_by_id(tasks, task_id)
    _init_history(task)
    return task


def log_task_update(tasks, task_id, field, old_value, new_value):
    if field not in {"title", "description"}:
        raise TaskValidationError("Invalid field for update history")
    task = _get_task_by_id(tasks, task_id)
    details = {"field": field, "old": old_value, "new": new_value}
    _add_history_event(task, "updated", details)
    return task


def log_status_change(tasks, task_id, old_status, new_status):
    task = _get_task_by_id(tasks, task_id)
    details = {"old_status": old_status, "new_status": new_status}
    _add_history_event(task, "status_changed", details)
    return task


def log_assignment_change(tasks, task_id, assigned_user=None, removed_user=None):
    task = _get_task_by_id(tasks, task_id)
    details = {}
    if assigned_user:
        details["assigned"] = assigned_user
    if removed_user:
        details["removed"] = removed_user
    if not details:
        raise TaskValidationError("Assignment change requires assigned_user or removed_user")
    _add_history_event(task, "assignment_changed", details)
    return task


def log_deadline_change(tasks, task_id, old_deadline, new_deadline):
    task = _get_task_by_id(tasks, task_id)
    details = {"old_deadline": old_deadline, "new_deadline": new_deadline}
    _add_history_event(task, "deadline_changed", details)
    return task


def log_priority_change(tasks, task_id, old_priority, new_priority):
    task = _get_task_by_id(tasks, task_id)
    details = {"old_priority": old_priority, "new_priority": new_priority}
    _add_history_event(task, "priority_changed", details)
    return task


def log_tags_change(tasks, task_id, old_tags, new_tags):
    task = _get_task_by_id(tasks, task_id)
    details = {"old_tags": old_tags, "new_tags": new_tags}
    _add_history_event(task, "tags_changed", details)
    return task


def get_history(tasks, task_id, page=1, per_page=10):
    task = _get_task_by_id(tasks, task_id)
    history = task.get("history", [])
    # Sort by timestamp desc
    sorted_history = sorted(history, key=lambda e: e["timestamp"], reverse=True)
    start = (page - 1) * per_page
    end = start + per_page
    return sorted_history[start:end]
