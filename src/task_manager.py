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


def _load_tasks(data_file=DATA_FILE) -> List[Dict]:
    """Charge les tâches depuis le fichier JSON"""
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            _save_tasks(DEFAULT_TASKS)
            return DEFAULT_TASKS.copy()
    else:
        _save_tasks(DEFAULT_TASKS)
        return DEFAULT_TASKS.copy()


def _save_tasks(tasks_to_save: List[Dict], data_file=DATA_FILE):
    """Sauvegarde les tâches dans le fichier JSON"""
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def get_tasks(
    page: int = 1, size: int = 20, data_file=DATA_FILE
) -> List[Dict]:
    """Récupère la liste des tâches"""
    tasks = _load_tasks(data_file=data_file)
    total_tasks = len(tasks)
    total_pages = (total_tasks + size - 1) // size if size else 1

    if not tasks:
        print("Total de tâches: {}".format(total_tasks))
        print("Total de pages: {}".format(total_pages))
        return [], total_tasks, total_pages

    if page > total_pages:
        print(f"Page {page} n'existe pas. Total de pages: {total_pages}")
        return [], total_tasks, total_pages
    if page < 1:
        raise ValueError("Invalid page size")

    start = (page - 1) * size
    end = start + size
    return tasks[start:end], total_tasks, total_pages


def create_task(
    title: str, description: str = "", data_file=DATA_FILE
) -> Dict:
    """Crée une nouvelle tâche avec validation"""
    title = title.strip()
    description = description.strip()

    if not title:
        raise TaskValidationError("Title is required")
    if len(title) > 100:
        raise TaskValidationError("Title cannot exceed 100 characters")
    if len(description) > 500:
        raise TaskValidationError("Description cannot exceed 500 characters")

    tasks = _load_tasks(data_file=data_file)
    next_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "TODO",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    tasks.append(new_task)
    _save_tasks(tasks, data_file=data_file)

    return new_task


def get_task_by_id(task_id: int) -> Dict:
    """Récupère une tâche par son ID"""
    task_list = _load_tasks()
    for task in task_list:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def modify_task(
    task_id: int,
    title: str = None,
    description: str = None,
    data_file=DATA_FILE,
    **kwargs,
) -> Dict:
    """Modifie une tâche existante.

    Seuls les champs `title` et `description` peuvent être modifiés.
    Les autres champs comme l'ID, le statut ou la date de création sont ignorés.
    """
    if kwargs:
        raise TaskValidationError(
            "Seuls le titre et la description peuvent être modifiés."
        )
    task_list = _load_tasks(data_file=data_file)
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

            _save_tasks(task_list, data_file=data_file)
            return task

    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def change_task_status(
    task_id: int, new_status: str, data_file=DATA_FILE
) -> Dict:
    """Change le statut d'une tâche existante"""
    if new_status not in VALID_STATUSES:
        raise TaskValidationError(
            "Invalid status. Allowed values: TODO, ONGOING, DONE"
        )

    tasks = _load_tasks(data_file=data_file)
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            _save_tasks(tasks, data_file=data_file)
            return task

    raise TaskNotFoundError("Task not found")


def delete_task(task_id: int, data_file=DATA_FILE):
    """Supprime définitivement une tâche existante par son ID"""
    tasks = _load_tasks(data_file=data_file)
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        raise TaskValidationError("Task not found")

    _save_tasks(updated_tasks, data_file=data_file)
    

def search_tasks(keyword, page=1, size=10, data_file=DATA_FILE):
    tasks = _load_tasks(data_file)
    keyword = keyword.strip().lower()
    if keyword:
        filtered = [
            t for t in tasks
            if keyword in t["title"].lower() or keyword in t["description"].lower()
        ]
    else:
        filtered = tasks
    total_tasks = len(filtered)
    total_pages = (total_tasks + size - 1) // size if total_tasks > 0 else 0
    if page < 1 or size < 1:
        raise ValueError("Invalid page size")
    if page > total_pages and total_pages != 0:
        print(f"Page {page} n'existe pas. Total de pages: {total_pages}")
        return [], total_tasks, total_pages
    start = (page - 1) * size
    end = start + size
    return filtered[start:end], total_tasks, total_pages

