#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table

from task_manager import (
    get_tasks,
    create_task,
    TaskValidationError,
    get_task_by_id,
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
            task["status"],
            task["title"],
            task["description"],
            task["created_at"],
        )

    console.print(table)


@cli.command()
@click.option(
    "--title", prompt="Titre", help="Titre de la tâche (obligatoire)"
)
@click.option(
    "--description", default="", help="Description de la tâche (optionnelle)"
)
def create(title, description):
    """Créer une nouvelle tâche"""
    try:
        task = create_task(title, description)
        console.print(
            f"Tâche créée avec succès (ID: {task['id']})", style="green"
        )
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")


@cli.command()
@click.argument("task_id", type=int)
def show(task_id):
    """Afficher une tâche par son ID"""
    task = get_task_by_id(task_id)
    table = Table(title=f"Tâche {task['id']}")
    table.add_column("Champ", style="cyan")
    table.add_column("Valeur", style="white")

    table.add_row("ID", str(task["id"]))
    table.add_row("Statut", task["status"])
    table.add_row("Titre", task["title"])
    table.add_row("Description", task["description"])
    table.add_row("Créée le", task["created_at"])

    console.print(table)


if __name__ == "__main__":
    console.print(
        "Gestionnaire de Tâches - Version CLI Python\n", style="bold blue"
    )
    cli()
