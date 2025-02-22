import json
from pathlib import Path
import typer

cli = typer.Typer()
DATA_FILE = Path.home() / ".todo.json"  # Store tasks in the user's home directory

# Ensure the data file exists
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")


def read_tasks():
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []


def write_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=4))


@cli.command()
def add(task: str):
    """Add a new task to the list."""
    tasks = read_tasks()
    tasks.append({"task": task, "completed": False})
    write_tasks(tasks)
    typer.echo(f"✅ Task added: {task}")


@cli.command(name="list")
def list_tasks():
    """List all tasks."""
    tasks = read_tasks()
    if not tasks:
        typer.echo("📭 No tasks found.")
        return

    typer.echo("\n📝 To-Do List:")
    for idx, task in enumerate(tasks, start=1):
        status = "✔️" if task["completed"] else "❌"
        typer.echo(f"{idx}. {task['task']} [{status}]")


@cli.command()
def complete(task_number: int):
    """Mark a task as completed."""
    tasks = read_tasks()
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        write_tasks(tasks)
        typer.echo(f"🎯 Task {task_number} marked as completed.")
    else:
        typer.echo("⚠️ Invalid task number.")


@cli.command()
def delete(task_number: int):
    """Delete a task from the list."""
    tasks = read_tasks()
    if 1 <= task_number <= len(tasks):
        deleted_task = tasks.pop(task_number - 1)
        write_tasks(tasks)
        typer.echo(f"🗑️ Task deleted: {deleted_task['task']}")
    else:
        typer.echo("⚠️ Invalid task number.")


def main():
    cli()


if __name__ == "__main__":
    main()
