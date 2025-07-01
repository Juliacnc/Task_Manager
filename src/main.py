#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table

from task_manager import (
    get_tasks,
    create_task,
    change_task_status,
    delete_task,
    TaskValidationError,
    get_task_by_id,
    modify_task,
    TaskNotFoundError,
)

console = Console()


@click.group()
def cli():
    """Gestionnaire de Tâches - Version CLI Python"""
    pass


@click.option("--page", default=1, help="Numéro de page (commence à 1)")
@click.option("--size", default=10, help="Nombre de tâches par page")
@cli.command()
def list(page, size):
    """Lister les tâches"""
    tasks, total_tasks, total_pages = get_tasks(page=page, size=size)

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
    console.print(
        f"Page {page}/{total_pages} - Total de tâches : {total_tasks}"
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
def delete(task_id):
    """Supprime une tâche par son ID"""
    try:
        delete_task(task_id)
        console.print(
            f"Tâche ID {task_id} supprimée avec succès.", style="green"
        )
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Supprime une tâche par son ID"""
    try:
        delete_task(task_id)
        console.print(
            f"Tâche ID {task_id} supprimée avec succès.", style="green"
        )
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")


@cli.command()
@click.argument("task_id", type=int)
@click.argument(
    "new_status",
    type=click.Choice(["TODO", "ONGOING", "DONE"], case_sensitive=True),
)
def update_status(task_id, new_status):
    """Changer le statut d'une tâche"""
    try:
        task = change_task_status(task_id, new_status)
        console.print(
            f"Tâche {task['id']} mise à jour avec le statut : [green]{task['status']}[/green]"
        )
    except TaskValidationError as e:
        console.print(f"Erreur de validation : {e}", style="red")
    except TaskNotFoundError as e:
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


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", default="", help="Titre à modifier")
@click.option("--description", default="", help="Description à modifier")
@click.option(
    "--id",
    default=None,
    help="Modification du champ 'id' non autorisée",
    required=False,
)
@click.option(
    "--status",
    default=None,
    help="Modification du champ 'status' non autorisée",
    required=False,
)
@click.option(
    "--created_at",
    default=None,
    help="Modification du champ 'created_at' non autorisée",
    required=False,
)
def modify(task_id, title, description, id, status, created_at):
    """Modifier une tâche existante"""
    forbidden_fields = []
    if id is not None:
        forbidden_fields.append("id")
    if status is not None:
        forbidden_fields.append("status")
    if created_at is not None:
        forbidden_fields.append("created_at")
    if forbidden_fields:
        console.print(
            f"Erreur : Seuls les champs 'title' et 'description' "
            f"peuvent être modifiés"
            f"Champs non autorisés détectés : {', '.join(forbidden_fields)}",
            style="red",
        )
        return
    try:
        task = modify_task(task_id, title, description)
        console.print(
            f"Tâche {task['id']} modifiée avec succès", style="green"
        )
    except ValueError as e:
        console.print(f"Erreur : {e}", style="red")
    except TaskValidationError as e:
        console.print(f"Erreur de validation : {e}", style="red")


if __name__ == "__main__":
    console.print(
        "Gestionnaire de Tâches - Version CLI Python\n", style="bold blue"
    )
    cli()
