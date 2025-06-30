from typing import List, Dict

# DB
task_list = [
    {
        "id": 1,
        "title": "Première tâche",
        "description": "Description de la première tâche",
        "status": "TODO",
    },
    {
        "id": 2,
        "title": "Deuxième tâche",
        "description": "Description de la deuxième tâche",
        "status": "DONE",
    },
]


def get_tasks() -> List[Dict]:
    """Récupère la liste des tâches"""
    return task_list


def modify_task(
    task_id: int, title: str, description: str, status: str
) -> Dict:
    """Modifie une tâche existante"""
    for task in task_list:
        if task["id"] == task_id:
            task["title"] = title
            task["description"] = description
            task["status"] = status
            return task

    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")
