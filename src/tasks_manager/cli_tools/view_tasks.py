import click
from src.tasks_manager.utils.query_utils import (
    get_tasks,
    filter_by_id,
    filter_tasks_by_status,
    search_tasks,
    sorted_task,
)
from src.tasks_manager.utils.file_utils import display_tasks
from src.classes.errors import TaskNotFoundError


@click.command(name="view_tasks")
@click.option(
    "--status",
    type=click.Choice(["TODO", "ONGOING", "DONE"]),
    help="Filtrer par statut",
)
@click.option("--id", type=int, help="Afficher une tâche par ID")
@click.option(
    "--search",
    type=str,
    help="Mot-clé à rechercher dans le titre ou la description",
)
@click.option(
    "--sort_by",
    type=click.Choice(["title", "created_at", "status"]),
    default="created_at",
)
@click.option("--asc/--desc", default=True, help="Ordre croissant/décroissant")
@click.option("--page", default=1, help="Numéro de la page")
@click.option("--size", default=10, help="Nombre de tâches par page")
@click.pass_context
def view_tasks(ctx, status, id, search, sort_by, asc, page, size):
    """Affiche les tâches avec options de filtre, tri et pagination"""
    tasks_list = ctx.obj["tasks_list"]

    try:
        # Si recherche par ID, priorité
        if id is not None:
            task = filter_by_id(id, tasks_list)
            click.echo(
                f"[{task['id']}] {task['title']} ({task['status']}) - {task['description']}"
            )
            return

        # Filtrage
        if status:
            tasks_list = filter_tasks_by_status(status, tasks_list)

        if search:
            tasks_list = search_tasks(search, tasks_list)

        if sort_by:
            tasks_list = sorted_task(
                tasks_list, sort_by=sort_by, ascending=asc
            )

        # Pagination
        paginated_tasks, total_tasks, total_pages = get_tasks(
            page, size, tasks_list
        )
        display_tasks(paginated_tasks, page, total_pages, total_tasks)

    except TaskNotFoundError as e:
        click.echo(str(e), err=True)
    except Exception as e:
        click.echo(f"Erreur : {e}", err=True)
