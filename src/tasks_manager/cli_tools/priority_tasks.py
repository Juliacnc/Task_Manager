import click
from src.tasks_manager.utils.priority_manager import task_priority
from src.tasks_manager.utils.file_utils import display_tasks


@click.command(name="priority_manager")
@click.argument("task_id", type=int)
@click.argument("action", type=click.Choice(["set", "get", "sort", "filter"]))
@click.option(
    "--priority",
    type=click.Choice(["LOW", "NORMAL", "HIGH", "CRITICAL"]),
    help="Priority to set for the task (required for 'set' and 'filter' actions).",
)
@click.pass_context
def manage_priority(ctx, task_id: int, action: str, priority: str = None):
    task_list = ctx.obj.get("task_list")

    updated_task, updated_tasks_list = task_priority(
        task_list, task_id, action, priority
    )

    display_tasks(
        updated_tasks_list,
        page=1,
        total_pages=1,
        total_tasks=len(updated_tasks_list),
    )
