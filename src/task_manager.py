import click
from pathlib import Path
import sys


sys.path.append(str(Path(__file__).parent.parent))

from src.tasks_manager.utils.file_utils import _load_tasks, _save_tasks
from src.tasks_manager.cli_tools.cli_data_manager import (
    create_task,
    modify_task,
    change_task_status,
    delete_task,
)
from src.tasks_manager.cli_tools.view_tasks import view_tasks
from src.tasks_manager.cli_tools.task_sheduler import task_deadline
from src.tasks_manager.cli_tools.tags import tags_cli
from src.tasks_manager.cli_tools.priority_tasks import manage_priority


@click.group()
@click.pass_context
def task_manager(ctx):
    """Gestionnaire de Tâches - Version CLI Python"""
    # Charge les tâches une fois et les met dans le contexte Click
    ctx.ensure_object(dict)
    ctx.obj["tasks_list"] = _load_tasks(data_file="tasks.json")


@task_manager.result_callback()
@click.pass_context
def save_tasks(ctx, result, **kwargs):
    """Sauvegarde les tâches modifiées automatiquement si besoin"""
    tasks_list = ctx.obj.get("tasks_list")
    if tasks_list is not None:
        _save_tasks(tasks_list, data_file="tasks.json")


# Ajout des sous-commandes
task_manager.add_command(create_task)
task_manager.add_command(modify_task)
task_manager.add_command(change_task_status)
task_manager.add_command(delete_task)
task_manager.add_command(view_tasks)
task_manager.add_command(task_deadline)
task_manager.add_command(tags_cli)
task_manager.add_command(manage_priority)

if __name__ == "__main__":
    task_manager(obj={})
