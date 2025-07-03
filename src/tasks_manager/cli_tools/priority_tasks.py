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
    tasks_list = ctx.obj["tasks_list"]

    updated_task = task_priority(tasks_list, task_id, action, priority)

    # update the task in the tasks list
    tasks_list = [
        task if task["id"] != task_id else updated_task for task in tasks_list
    ]
    ctx.obj["tasks_list"] = tasks_list

    display_tasks(
        [updated_task],
        page=1,
        total_pages=1,
        total_tasks=1,
    )
