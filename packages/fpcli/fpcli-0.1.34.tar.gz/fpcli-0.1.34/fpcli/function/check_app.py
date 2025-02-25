
from pathlib import Path
import typer
from ..fpcli_settings import APP_FOLDER

def check_app(app_name: str):
    base_dir = Path(APP_FOLDER).resolve()  # Root directory where apps are stored
    app_dir = base_dir / app_name
    if not app_dir.exists():
        typer.echo(typer.style(f"App '{app_name}' does not exist. Please create it first!",fg=typer.colors.RED,bold=True))
        raise typer.Exit()
    return app_dir

def is_exits(app_name: str):
    base_dir = Path(APP_FOLDER).resolve()  # Root directory where apps are stored
    app_dir = base_dir / app_name
    if app_dir.exists():
        typer.echo(typer.style(f"App '{app_name}' alredy exist. on {app_dir}",fg=typer.colors.RED,bold=True))
        raise typer.Exit()
