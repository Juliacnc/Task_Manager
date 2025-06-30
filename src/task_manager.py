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
        "created_at": "2024-01-01T10:00:00"
    },
    {
        "id": 2,
        "title": "Deuxième tâche",
        "description": "Description de la deuxième tâche",
        "status": "DONE",
        "created_at": "2024-01-02T15:00:00"
    }
]


class TaskValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    pass


def _load_tasks() -> List[Dict]:
    """Charge les tâches depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
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
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
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
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    tasks.append(new_task)
    _save_tasks(tasks)

    return new_task


def delete_task(task_id: int):
    """Supprime définitivement une tâche existante par son ID"""
    tasks = _load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        raise TaskValidationError("Task not found")

    _save_tasks(updated_tasks)
