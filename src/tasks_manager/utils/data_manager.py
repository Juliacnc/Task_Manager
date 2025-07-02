from typing import List, Dict, Tuple
from datetime import datetime

from src.classes.errors import (
    TaskValidationError,
    TaskNotFoundError,
)


VALID_STATUSES = {"TODO", "ONGOING", "DONE"}


def _create_task(
    title: str,
    description: str = "",
    tasks_list: List[Dict] = None,
) -> Tuple[Dict, List[Dict]]:
    """Crée une nouvelle tâche"""
    if tasks_list is None:
        tasks_list = []

    title = title.strip()
    description = description.strip()

    if not title:
        raise TaskValidationError("Title is required")
    if len(title) > 100:
        raise TaskValidationError(
            "Le titre ne peut pas dépasser 100 caractères"
        )
    if len(description) > 500:
        raise TaskValidationError(
            "La description ne peut pas dépasser 500 caractères"
        )

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


def _modify_task(
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
                    raise TaskValidationError(
                        "Le titre ne peut pas dépasser 100 caractères"
                    )
                task["title"] = title
            if description is not None:
                description = description.strip()
                if len(description) > 500:
                    raise TaskValidationError(
                        "La description ne peut pas dépasser 500 caractères"
                    )
                task["description"] = description

            return task, tasks_list


def _change_task_status(
    tasks_list: List[Dict],
    task_id: int,
    new_status: str,
) -> Tuple[Dict, List[Dict]]:
    """Change le statut d'une tâche existante"""
    print(new_status)
    if new_status not in VALID_STATUSES:
        raise TaskValidationError(
            "Statut invalide. Valeurs autorisées : TODO, ONGOING, DONE"
        )

    for task in tasks_list:
        if task["id"] == task_id:
            task["status"] = new_status
            return task, tasks_list

    raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")


def _delete_task(task_id: int, tasks_list: List[Dict]) -> List[Dict]:
    """Supprime une tâche par son ID et retourne la liste mise à jour"""
    updated_tasks = [task for task in tasks_list if task["id"] != task_id]

    if len(updated_tasks) == len(tasks_list):
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")

    return updated_tasks
