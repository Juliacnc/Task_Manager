import click
from src.tasks_manager.utils.data_manager import (
    _create_task,
    _modify_task,
    _change_task_status,
    _delete_task,
)


@click.command(name="create_task")
@click.option("--title", prompt="Title", help="Title of the task")
@click.option("--description", default="", help="Description of the task")
@click.pass_context
def create_task(ctx, title: str, description: str = ""):
    """Crée une nouvelle tâche"""
    tasks_list = ctx.obj["tasks_list"]
    new_task, updated_list = _create_task(title, description, tasks_list)
    ctx.obj["tasks_list"] = updated_list
    click.echo(f"Tâche créée : {new_task['title']}")


@click.command(name="modify_task")
@click.argument("task_id", type=int)
@click.option("--title", default=None, help="New title of the task")
@click.option(
    "--description", default=None, help="New description of the task"
)
@click.pass_context
def modify_task(ctx, task_id: int, title: str = None, description: str = None):
    """Modifie une tâche existante"""
    tasks_list = ctx.obj["tasks_list"]
    new_task, updated_list = _modify_task(
        tasks_list, task_id, title=title, description=description
    )
    ctx.obj["tasks_list"] = updated_list
    click.echo(f"Tâche modifiée : {new_task['title']}")


@click.command(name="change_task_status")
@click.argument("task_id", type=int)
@click.option(
    "--status",
    required=True,
    help="New status of the task",
)
@click.pass_context
def change_task_status(ctx, task_id: int, status: str):
    """Change le statut d'une tâche"""
    tasks_list = ctx.obj["tasks_list"]
    updated_task, updated_list = _change_task_status(
        tasks_list, task_id, status
    )
    ctx.obj["tasks_list"] = updated_list
    click.echo(
        f"Statut de la tâche {updated_task['id']} changé en {updated_task['status']}"
    )


@click.command(name="delete_task")
@click.argument("task_id", type=int)
@click.pass_context
def delete_task(ctx, task_id: int):
    """Supprime une tâche existante"""
    tasks_list = ctx.obj["tasks_list"]
    updated_list = _delete_task(task_id, tasks_list)
    ctx.obj["tasks_list"] = updated_list
    click.echo(f"Tâche avec l'ID {task_id} supprimée")
