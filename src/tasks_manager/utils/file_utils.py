"""Module utils for Task Manager application."""

import json
import os
from typing import List, Dict
from rich.console import Console
from rich.table import Table

console = Console()

DATA_FILE = "tasks.json"


def _load_tasks(data_file=DATA_FILE) -> List[Dict]:
    """Charge les tâches depuis le fichier JSON"""
    if not os.path.exists(data_file):
        json.dump(
            [],
            open(data_file, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=2,
        )
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_tasks(tasks_to_save: List[Dict], data_file=DATA_FILE):
    """Sauvegarde les tâches dans le fichier JSON"""
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def display_tasks(
    tasks: List[Dict], page: int, total_pages: int, total_tasks: int
):
    table = Table(title=f"Liste des tâches (page {page}/{total_pages})")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Statut", style="green")
    table.add_column("Titre", style="white")
    table.add_column("Description", style="dim", overflow="fold")
    table.add_column("Créée le", style="magenta")
    table.add_column("Echéance", style="yellow", no_wrap=True)
    table.add_column("Tags", style="blue")

    for task in tasks:
        table.add_row(
            str(task["id"]),
            task["status"],
            task["title"],
            task["description"],
            task["created_at"],
            task.get("deadline", "Aucune"),
            ", ".join(task.get("tags", [])) if task.get("tags") else "Aucun",
        )

    console.print(table)
    console.print(
        f"Page {page} sur {total_pages} — Total de tâches : {total_tasks}",
        style="bold",
    )
