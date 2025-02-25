import typer
import shutil
import time
from pathlib import Path
from .basic import app
from ..fpcli_settings import APP_FOLDER
from ..function.get_settings import get_settings_class

# Define installed apps list (Modify this based on how apps are registered in your project)


def get_app_static_dirs() -> dict[str, Path]:
    settings_class = get_settings_class()

    INSTALLED_APPS = settings_class.INSTALLED_APPS  # Example: List of app names
    base_dir = Path(f"{APP_FOLDER}").resolve()
    """Finds static directories inside installed apps."""
    static_dirs = {}
    for app_name in INSTALLED_APPS:
        app_path = base_dir / app_name / "static"
        if app_path.exists() and app_path.is_dir():
            static_dirs[app_name] = app_path
    return static_dirs


def copy_static_files(app_static_dirs: dict[str, Path], dest_dir: Path, verbose: bool):
    """Copies static files from app-specific static folders into a structured destination."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    for app_name, src_dir in app_static_dirs.items():
        app_static_dest = dest_dir / app_name  # Create a folder per app
        app_static_dest.mkdir(parents=True, exist_ok=True)

        for item in src_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(src_dir)
                destination = app_static_dest / relative_path

                # Ensure destination directory exists
                destination.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(item, destination)
                if verbose:
                    typer.echo(f"Copied {item} -> {destination}")


def watch_static_files(app_static_dirs: dict[str, Path], dest_dir: Path):
    """Watches static files for changes and updates them accordingly."""
    last_modified_times = {}
    while True:
        for app_name, src_dir in app_static_dirs.items():
            for item in src_dir.rglob("*"):
                if item.is_file():
                    mod_time = item.stat().st_mtime
                    if last_modified_times.get(item) != mod_time:
                        last_modified_times[item] = mod_time
                        relative_path = item.relative_to(src_dir)
                        destination = dest_dir / app_name / relative_path
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, destination)
                        typer.echo(f"Updated {item} -> {destination}")
        time.sleep(1)


@app.command()
def collectstatic(
    destination: Path = typer.Argument(
        "static", help="Destination directory for collected static files"
    ),
    clear: bool = typer.Option(
        True, "--clear", help="Clear the destination directory before copying"
    ),
    watch: bool = typer.Option(
        False, "--watch", help="Monitor file changes in real time"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="check the details of the files"
    ),
):
    """Collects static files from installed apps and organizes them by app name within the destination directory (default: static). When the --watch flag is passed, it monitors file changes in real time."""
    typer.echo("🚀 Static file collection started.....")

    app_static_dirs = get_app_static_dirs()

    if clear and destination.exists():
        shutil.rmtree(destination)
        # typer.echo(f"Cleared {destination}")

    if not app_static_dirs:
        typer.echo("No static directories found in installed apps.")
        raise typer.Exit(1)

    copy_static_files(app_static_dirs, destination, verbose=verbose)
    typer.echo(
        typer.style(
            "🎉 Static files collection completed.", typer.colors.GREEN, bold=True
        )
    )

    if watch:
        typer.echo("Watching for file changes...")
        watch_static_files(app_static_dirs, destination)
