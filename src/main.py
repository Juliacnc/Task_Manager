#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table
from datetime import datetime

from task_manager import (
    get_tasks,
    create_task,
    change_task_status,
    delete_task,
    TaskValidationError,
    get_task_by_id,
    modify_task,
    TaskNotFoundError,
    _load_tasks,
    _save_tasks,
)

console = Console()

# Chargement unique au démarrage
tasks_list = _load_tasks(data_file="tasks.json")


def get_tasks_sorted_filtered(
    page=1,
    size=10,
    sort_by="created_at",
    order="desc",
    status_filter=None,
    tasks_list=None,
):
    if tasks_list is None:
        tasks_list = []

    tasks = tasks_list

    # Filtrer par statut si demandé
    if status_filter:
        if status_filter not in ["TODO", "ONGOING", "DONE"]:
            raise TaskValidationError("Invalid status filter")
        tasks = [t for t in tasks if t["status"] == status_filter]

    valid_sort = {"created_at", "title", "status"}
    if sort_by not in valid_sort:
        raise TaskValidationError("Invalid sort criteria")

    reverse = order == "desc"

    if sort_by == "status":
        order_map = {"TODO": 0, "ONGOING": 1, "DONE": 2}
        tasks.sort(key=lambda t: order_map[t["status"]], reverse=reverse)
    elif sort_by == "created_at":
        tasks.sort(key=lambda t: datetime.fromisoformat(t["created_at"]), reverse=reverse)
    else:  # tri alphabétique sur titre
        tasks.sort(key=lambda t: t["title"].lower(), reverse=reverse)

    total_tasks = len(tasks)
    total_pages = (total_tasks + size - 1) // size if size else 1

    if page < 1 or (page > total_pages and total_pages != 0):
        raise ValueError(f"Page {page} does not exist (max {total_pages})")

    start = (page - 1) * size
    end = start + size
    return tasks[start:end], total_tasks, total_pages


@click.group()
def cli():
    """Gestionnaire de Tâches - Version CLI Python"""
    pass


@cli.command()
@click.option("--page", default=1, help="Numéro de page (commence à 1)")
@click.option("--size", default=10, help="Nombre de tâches par page")
@click.option(
    "--sort-by",
    default="created_at",
    type=click.Choice(["created_at", "title", "status"]),
    help="Critère de tri",
)
@click.option(
    "--order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Ordre du tri (ascendant ou descendant)",
)
@click.option(
    "--status",
    default=None,
    type=click.Choice(["TODO", "ONGOING", "DONE"]),
    help="Filtrer par statut (optionnel)",
)
def list(page, size, sort_by, order, status):
    """Lister les tâches, avec options de tri et filtre"""
    try:
        tasks, total_tasks, total_pages = get_tasks_sorted_filtered(
            page=page,
            size=size,
            sort_by=sort_by,
            order=order,
            status_filter=status,
            tasks_list=tasks_list,
        )
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")
        return
    except ValueError as e:
        console.print(f"Erreur : {e}", style="red")
        return

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
    console.print(f"Page {page}/{total_pages} - Total de tâches : {total_tasks}")

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
    global tasks_list
    try:
        new_task, tasks_list = create_task(
            title, description, tasks_list=tasks_list
        )
        _save_tasks(tasks_list, data_file="tasks.json")
        console.print(
            f"Tâche créée avec succès (ID: {new_task['id']})", style="green"
        )
    except TaskValidationError as e:
        console.print(f"Erreur : {e}", style="red")


@cli.command()
@click.argument("task_id", type=int)
@click.argument("title", type=str)
@click.argument("description", type=str)
def modify(task_id, title, description):
    """Modifier une tâche existante"""
    global tasks_list
    try:
        task, tasks_list = modify_task(
            tasks_list=tasks_list,
            task_id=task_id,
            title=title,
            description=description,
        )
        _save_tasks(tasks_list, data_file="tasks.json")
        console.print(
            f"Tâche {task['id']} modifiée avec succès", style="green"
        )
    except ValueError as e:
        console.print(f"Erreur : {e}", style="red")
    except TaskValidationError as e:
        console.print(f"Erreur de validation : {e}", style="red")


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
def modify(
    task_id, title, description, id, status, created_at
):
    """Modifier une tâche existante"""
    global tasks_list
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
            f"peuvent être modifiés. Champs non autorisés détectés : {', '.join(forbidden_fields)}",
            style="red",
        )
        return
    try:
        task, tasks_list = modify_task(
            tasks_list=tasks_list,
            task_id=task_id,
            title=title,
            description=description,
        )
        _save_tasks(tasks_list, data_file="tasks.json")
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
