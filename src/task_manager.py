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
    print(os.path.exists(data_file))
    if os.path.exists(data_file):
        # try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # except (json.JSONDecodeError, IOError):
    #     _save_tasks(DEFAULT_TASKS)
    #     return DEFAULT_TASKS.copy()
    # else:
    #     _save_tasks(DEFAULT_TASKS)
    #     return DEFAULT_TASKS.copy()


def _save_tasks(tasks_to_save: List[Dict], data_file=DATA_FILE):
    """Sauvegarde les tâches dans le fichier JSON"""
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def get_tasks(
    page: int = 1, size: int = 20, tasks_list: List[Dict] = None
) -> List[Dict]:
    """Récupère la liste des tâches"""
    # tasks = _load_tasks(data_file=data_file)
    total_tasks = len(tasks_list)
    total_pages = (total_tasks + size - 1) // size if size else 1

    if not tasks_list:
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
    return tasks_list[start:end], total_tasks, total_pages


def create_task(
    title: str,
    description: str = "",
    tasks_list: List[Dict] = None,
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

    next_id = max([task["id"] for task in tasks_list], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "TODO",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    tasks_list.append(new_task)

    return new_task, tasks_list


def get_task_by_id(task_id: int, tasks_list) -> Dict:
    """Récupère une tâche par son ID"""
    for task in tasks_list:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def modify_task(
    tasks_list: List[Dict],
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
    for task in tasks_list:
        if task["id"] == task_id:
            if title is not None:
                if title.strip() == "":
                    raise TaskValidationError("Title is required")
                task["title"] = title.strip()
            if description is not None:
                task["description"] = description.strip()

            if len(task["title"]) > 100:
                raise TaskValidationError("Title cannot exceed 100 characters")
            if len(task["description"]) > 500:
                raise TaskValidationError(
                    "Description cannot exceed 500 characters"
                )

            return task, tasks_list

    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")


def change_task_status(
    task_id: int, new_status: str, tasks_list: List[Dict]
) -> Dict:
    """Change le statut d'une tâche existante"""
    if new_status not in VALID_STATUSES:
        raise TaskValidationError(
            "Invalid status. Allowed values: TODO, ONGOING, DONE"
        )

    for task in tasks_list:
        if task["id"] == task_id:
            task["status"] = new_status
            return task, tasks_list

    raise TaskNotFoundError("Task not found")


def delete_task(task_id: int, tasks_list: List[Dict]):
    """Supprime définitivement une tâche existante par son ID"""
    updated_tasks = [task for task in tasks_list if task["id"] != task_id]

    if len(updated_tasks) == len(tasks_list):
        raise TaskValidationError("Task not found")

    return updated_tasks


def search_tasks(keyword, tasks_list, page=1, size=10) -> List[Dict]:
    keyword = keyword.strip().lower()
    if keyword:
        filtered = [
            t
            for t in tasks_list
            if keyword in t["title"].lower()
            or keyword in t["description"].lower()
        ]
    else:
        filtered = tasks_list
    task_range, total_tasks, total_pages = get_tasks(
        page=page, size=size, tasks_list=filtered
    )
    return task_range, total_tasks, total_pages
