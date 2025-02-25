
from pathlib import Path
import typer


def check_class(file_path: Path, class_name: str, app_name: str):
    if file_path.exists():
        typer.echo(
           typer.style( f"'{class_name}' already exists in app '{app_name}' path {file_path}!",typer.colors.RED,bold=True)
        )
        raise typer.Exit()