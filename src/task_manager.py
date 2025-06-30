import json
import os
from typing import List, Dict
from datetime import datetime

DATA_FILE = "tasks.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "title": "Première tâche",
        "description": "Description de la première tâche",
        "status": "TODO",
        "created_at": "2024-01-01T10:00:00",
    },
    {
        "id": 2,
        "title": "Deuxième tâche",
        "description": "Description de la deuxième tâche",
        "status": "DONE",
        "created_at": "2024-01-02T15:00:00",
    },
]


class TaskValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""

    pass


class TaskNotFoundError(Exception):
    """Exception personnalisée pour tâche non trouvée"""

    pass


VALID_STATUSES = {"TODO", "ONGOING", "DONE"}


def _load_tasks() -> List[Dict]:
    """Charge les tâches depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            _save_tasks(DEFAULT_TASKS)
            return DEFAULT_TASKS.copy()
    else:
        _save_tasks(DEFAULT_TASKS)
        return DEFAULT_TASKS.copy()


def _save_tasks(tasks_to_save: List[Dict]):
    """Sauvegarde les tâches dans le fichier JSON"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def get_tasks() -> List[Dict]:
    """Récupère la liste des tâches"""
    return _load_tasks()


def create_task(title: str, description: str = "") -> Dict:
    """Crée une nouvelle tâche avec validation"""
    title = title.strip()
    description = description.strip()

    if not title:
        raise TaskValidationError("Title is required")
    if len(title) > 100:
        raise TaskValidationError("Title cannot exceed 100 characters")
    if len(description) > 500:
        raise TaskValidationError("Description cannot exceed 500 characters")

    tasks = _load_tasks()
    next_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "TODO",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    tasks.append(new_task)
    _save_tasks(tasks)

    return new_task


def get_task_by_id(task_id: int) -> Dict:
    """Récupère une tâche par son ID"""
    task_list = _load_tasks()
    for task in task_list:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def modify_task(
    task_id: int, title: str = None, description: str = None, **kwargs
) -> Dict:
    """Modifie une tâche existante.

    Seuls les champs `title` et `description` peuvent être modifiés.
    Les autres champs comme l'ID, le statut ou la date de création sont ignorés.
    """
    if kwargs:
        raise TaskValidationError(
            "Seuls le titre et la description peuvent être modifiés."
        )
    task_list = _load_tasks()
    for task in task_list:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title.strip()
            if description is not None:
                task["description"] = description.strip()

            if not task["title"]:
                raise TaskValidationError("Title is required")
            if len(task["title"]) > 100:
                raise TaskValidationError("Title cannot exceed 100 characters")
            if len(task["description"]) > 500:
                raise TaskValidationError(
                    "Description cannot exceed 500 characters"
                )

            _save_tasks(task_list)
            return task

    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def change_task_status(task_id: int, new_status: str) -> Dict:
    """Change le statut d'une tâche existante"""
    if new_status not in VALID_STATUSES:
        raise TaskValidationError(
            "Invalid status. Allowed values: TODO, ONGOING, DONE"
        )

    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            _save_tasks(tasks)
            return task

    raise TaskNotFoundError("Task not found")


def delete_task(task_id: int):
    """Supprime définitivement une tâche existante par son ID"""
    tasks = _load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        raise TaskValidationError("Task not found")

    _save_tasks(updated_tasks)
