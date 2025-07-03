import click
from src.tasks_manager.utils.task_tags import tags_manager
from src.tasks_manager.utils.file_utils import display_tasks


@click.command(name="tags_manager")
@click.argument("task_id", type=int)
@click.argument(
    "action", type=click.Choice(["add", "remove", "filter", "get_all_tags"])
)
@click.argument("tags", nargs=-1)
@click.pass_context
def tags_cli(ctx, task_id, action, tags):
    """Manage tags for a specific task.

    ACTION can be 'add', 'remove', 'filter', or 'get_all_tags'.
    """
    tasks_list = ctx.obj["tasks_list"]

    if action == "add" and not tags:
        click.echo("No tags provided to add.")
        return

    if action == "remove" and not tags:
        click.echo("No tag provided to remove.")
        return

    updated_task, updated_tasks_list = tags_manager(
        tasks_list, task_id, action, list(tags)
    )

    click.get_current_context().obj["tasks_list"] = updated_tasks_list
    click.echo(f"Task {task_id} updated successfully with action '{action}'.")
    if action == "get_all_tags":
        click.echo("All tags with usage:")
        for tag, count in updated_task.items():
            click.echo(f"{tag}: {count}")

    if action == "filter":
        click.echo("Filtered tasks:")
        for task in updated_task:
            click.echo(f"Task ID: {task['id']}, Tags: {task.get('tags', [])}")

    display_tasks(
        updated_tasks_list,
        page=1,
        total_pages=1,
        total_tasks=len(updated_tasks_list),
    )
