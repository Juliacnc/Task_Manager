import json
import os
from typing import List, Dict, Tuple
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
            _save_tasks(DEFAULT_TASKS, data_file)
            return DEFAULT_TASKS.copy()
    else:
        _save_tasks(DEFAULT_TASKS, data_file)
        return DEFAULT_TASKS.copy()


def _save_tasks(tasks_to_save: List[Dict], data_file=DATA_FILE):
    """Sauvegarde les tâches dans le fichier JSON"""
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def get_tasks(
    page: int = 1, size: int = 20, tasks_list: List[Dict] = None
) -> Tuple[List[Dict], int, int]:
    """Récupère une page de tâches de la liste en mémoire"""
    if tasks_list is None:
        tasks_list = []

    total_tasks = len(tasks_list)
    total_pages = (total_tasks + size - 1) // size if size else 1

    if total_tasks == 0:
        return [], total_tasks, total_pages

    if page < 1 or page > total_pages:
        raise ValueError(f"Page {page} n'existe pas. Total de pages: {total_pages}")

    start = (page - 1) * size
    end = start + size
    return tasks_list[start:end], total_tasks, total_pages


def create_task(
    title: str,
    description: str = "",
    tasks_list: List[Dict] = None,
) -> Tuple[Dict, List[Dict]]:
    """Crée une nouvelle tâche avec validation, retourne la tâche créée et la liste modifiée"""
    if tasks_list is None:
        tasks_list = []

    title = title.strip()
    description = description.strip()

    if not title:
        raise TaskValidationError("Le titre est obligatoire")
    if len(title) > 100:
        raise TaskValidationError("Le titre ne peut pas dépasser 100 caractères")
    if len(description) > 500:
        raise TaskValidationError("La description ne peut pas dépasser 500 caractères")

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


def get_task_by_id(task_id: int, tasks_list: List[Dict]) -> Dict:
    """Récupère une tâche par son ID"""
    for task in tasks_list:
        if task["id"] == task_id:
            return task
    raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")


def modify_task(
    tasks_list: List[Dict],
    task_id: int,
    title: str = None,
    description: str = None,
    **kwargs,
) -> Tuple[Dict, List[Dict]]:
    """Modifie une tâche existante.

    Seuls les champs `title` et `description` peuvent être modifiés.
    Les autres champs sont ignorés.
    Retourne la tâche modifiée et la liste mise à jour.
    """
    if kwargs:
        raise TaskValidationError(
            "Seuls le titre et la description peuvent être modifiés."
        )
    for task in tasks_list:
        if task["id"] == task_id:
            if title is not None:
                title = title.strip()
                if title == "":
                    raise TaskValidationError("Le titre est obligatoire")
                if len(title) > 100:
                    raise TaskValidationError("Le titre ne peut pas dépasser 100 caractères")
                task["title"] = title
            if description is not None:
                description = description.strip()
                if len(description) > 500:
                    raise TaskValidationError("La description ne peut pas dépasser 500 caractères")
                task["description"] = description

            return task, tasks_list

    raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")


def change_task_status(
    task_id: int, new_status: str, tasks_list: List[Dict]
) -> Tuple[Dict, List[Dict]]:
    """Change le statut d'une tâche existante et retourne la tâche modifiée et la liste mise à jour"""
    if new_status not in VALID_STATUSES:
        raise TaskValidationError(
            "Statut invalide. Valeurs autorisées : TODO, ONGOING, DONE"
        )

    for task in tasks_list:
        if task["id"] == task_id:
            task["status"] = new_status
            return task, tasks_list

    raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")


def delete_task(task_id: int, tasks_list: List[Dict]) -> List[Dict]:
    """Supprime une tâche par son ID et retourne la liste mise à jour"""
    updated_tasks = [task for task in tasks_list if task["id"] != task_id]

    if len(updated_tasks) == len(tasks_list):
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")

    return updated_tasks
