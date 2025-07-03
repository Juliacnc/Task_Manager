import click

from src.tasks_manager.utils.task_deadline import DeadlineTask
from src.tasks_manager.utils.file_utils import display_tasks


@click.command(name="task_sheduler")
@click.argument("task_id", type=int)
@click.option(
    "--add_deadline",
    type=bool,
    default=False,
    is_flag=True,
    help="Add a deadline to the task in 'YYYY-MM-DD' format",
)
@click.option(
    "--modify_deadline",
    type=bool,
    default=False,
    is_flag=True,
    help="Modify the deadline of the task in 'YYYY-MM-DD' format",
)
@click.option(
    "--remove_deadline",
    type=bool,
    default=False,
    is_flag=True,
    help="Remove the deadline from the task",
)
@click.option(
    "--deadline",
    type=str,
    help="Deadline to be added or modified in 'YYYY-MM-DD' format",
)
@click.pass_context
def task_deadline(
    ctx, task_id, add_deadline, modify_deadline, remove_deadline, deadline
):
    """Manage deadlines for tasks."""
    tasks_list = ctx.obj["tasks_list"]

    deadline_task = DeadlineTask(
        task_list=tasks_list, task_id=task_id, deadline=deadline
    )

    if add_deadline:
        deadline_task.add_deadline_to_task()

        click.echo(f"Deadline '{deadline}' added to task ID {task_id}.")

    if modify_deadline:
        deadline_task.modify_task_deadline()
        click.echo(
            f"Deadline modified to '{modify_deadline}' for task ID {task_id}."
        )

    if remove_deadline:
        deadline_task.remove_deadline_from_task()
        click.echo(f"Deadline removed from task ID {task_id}.")

    task = deadline_task.task

    display_tasks([task], page=1, total_pages=1, total_tasks=len(tasks_list))
