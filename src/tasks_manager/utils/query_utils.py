from typing import List, Dict, Tuple

from src.classes.errors import (
    TaskNotFoundError,
)

VALID_STATUSES = {"TODO", "ONGOING", "DONE"}


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

    return filtered_tasks


def filter_by_id(task_id: int, tasks_list: List[Dict]) -> Dict:
    """Récupère une tâche par son ID"""
    for task in tasks_list:
        if task["id"] == task_id:
            return task
    raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")


def search_tasks(keyword, tasks_list) -> List[Dict]:
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

    return filtered


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
