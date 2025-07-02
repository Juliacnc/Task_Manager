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


def filter_tasks_by_status(
    status: str,
    tasks_list: List[Dict],
    page: int = 1,
    size: int = 20,
) -> Tuple[List[Dict], int, int]:
    """Filtre les tâches par statut avec pagination.

    :param status: Le statut à filtrer ("TODO", "ONGOING", "DONE")
    :param page: Numéro de la page (1-based)
    :param size: Nombre de tâches par page
    :param data_file: Fichier de données JSON
    :return: (liste des tâches filtrées pour la page, total de tâches filtrées, total de pages)
    """
    status = status.upper()
    if status not in VALID_STATUSES:
        raise ValueError("Invalid filter status")

    filtered_tasks = [task for task in tasks_list if task["status"] == status]

    task_range, total_tasks, total_pages = get_tasks(
        page=page, size=size, tasks_list=filtered_tasks
    )
    return task_range, total_tasks, total_pages


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


# def sorted_task(
#     tasks_list: List[Dict],
#     sort_by: str = "created_at",
#     ascending: bool = True,
# ) -> List[Dict]:
#     """Retourne les tâches triées par un champ spécifique"""
#     if sort_by not in ["id", "title", "status", "created_at"]:
#         raise ValueError("Invalid sort criteria.")
#     if sort_by == "status":
#         sorted_status = {
#             "TODO": 0,
#             "ONGOING": 1,
#             "DONE": 2,
#         }
#         tasks_list.sort(
#             key=lambda x: sorted_status[x[sort_by]], reverse=not ascending
#         )
#         return tasks_list


#     return sorted(tasks_list, key=lambda x: x[sort_by], reverse=not ascending)
def sorted_task(tasks_list, sort_by="created_at", ascending=True):
    if sort_by not in {"title", "created_at", "status"}:
        raise ValueError("Invalid sort criteria.")
    if sort_by == "status":
        status_order = {"DONE": 0, "ONGOING": 1, "TODO": 2}
        return sorted(
            tasks_list,
            key=lambda t: status_order.get(t["status"], 99),
            reverse=not ascending,
        )
    return sorted(
        tasks_list,
        key=lambda t: t[sort_by],
        reverse=not ascending,
    )
