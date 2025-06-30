from typing import List, Dict

# DB
task_list = [
    {
        "id": 1,
        "title": "Première tâche",
        "description": "Description de la première tâche",
        "status": "TODO"
    },
    {
        "id": 2,
        "title": "Deuxième tâche",
        "description": "Description de la deuxième tâche",
        "status": "DONE"
    }
]

def get_tasks() -> List[Dict]:
    """
    Récupère la liste des tâches
    """
    
    return task_list
