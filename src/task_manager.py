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


def get_task_by_id(task_id: int) -> Dict:
    """Récupère une tâche par son ID"""
    for task in task_list:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Tâche avec l'ID {task_id} non trouvée.")
