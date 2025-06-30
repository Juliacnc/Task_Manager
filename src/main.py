#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table

from task_manager import (
    get_tasks,
    TaskValidationError
)

console = Console()


@click.group()
def cli():
    """Gestionnaire de Tâches - Version CLI Python"""
    pass


@cli.command()
def list():
    """Lister les tâches"""
    try:
        result = get_tasks()
        
        if not result["tasks"]:
            console.print("Aucune tâche trouvée.", style="yellow")
            return
        
        table = Table(title="Liste des tâches")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Statut", style="green")
        table.add_column("Titre", style="white")
        table.add_column("Description", style="dim")
        
        for task in result["tasks"]:
            table.add_row(
                str(task["id"]),
                task['status'],
                task["title"],
                task["description"],
            )
        
        console.print(table)
 
    except TaskValidationError as e:
        console.print(f"Erreur: {e}", style="red")


if __name__ == '__main__':
    console.print("Gestionnaire de Tâches - Version CLI Python\n", style="bold blue")
    cli()
