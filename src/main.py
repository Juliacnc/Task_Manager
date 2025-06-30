#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table

from task_manager import (
    get_tasks,
    create_task,
    delete_task,
    TaskValidationError
)

console = Console()

@click.group()
def cli():
    """Gestionnaire de Tâches - Version CLI Python"""
    pass

@cli.command()
def list():
    """Lister les tâches"""
    tasks = get_tasks()

    if not tasks:
        console.print("Aucune tâche trouvée.", style="yellow")
        return

    table = Table(title="Liste des tâches")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Statut", style="green")
    table.add_column("Titre", style="white")
    table.add_column("Description", style="dim")
    table.add_column("Créée le", style="magenta")

    for task in tasks:
        table.add_row(
            str(task["id"]),
            task['status'],
            task["title"],
            task["description"],
            task["created_at"]
        )

    console.print(table)

@cli.command()
@click.option("--title", prompt="Titre", help="Titre de la tâche (obligatoire)")
@click.option("--description", default="", help="Description de la tâche (optionnelle)")
def create(title, description):
    """Créer une nouvelle tâche"""
    try:
        task = create_task(title, description)
        console.print(f"Tâche créée avec succès (ID: {task['id']})", style="green")
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")

@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Supprime une tâche par son ID"""
    try:
        delete_task(task_id)
        console.print(f"Tâche ID {task_id} supprimée avec succès.", style="green")
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")


if __name__ == '__main__':
    console.print("Gestionnaire de Tâches - Version CLI Python\n", style="bold blue")
    cli()
