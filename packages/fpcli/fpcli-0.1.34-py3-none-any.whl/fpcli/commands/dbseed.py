from pathlib import Path
import subprocess
import typer

from fpcli.function import check_app
from .basic import app
from ..fpcli_settings import APP_FOLDER


@app.command("dbseed")
def dbseed(
    app_name: str,
    reset: bool = typer.Option(False, "--reset", help="Clear database before seeding"),
):
    """Run all seeders from scratch. Optionally reset the database before seeding."""

    check_app(app_name)
    SEEDER_FOLDER: Path = Path(f"{APP_FOLDER}/{app_name}/seeders").resolve()

    if not SEEDER_FOLDER.exists():
        typer.echo(
            typer.style(
                "😥 No seeders found. Create them first!",
                typer.colors.YELLOW,
                bold=True,
            )
        )
        raise typer.Exit(1)

    subprocess.run(["python","-m", f"{APP_FOLDER.replace('/', '.')}{app_name}.seeders"])

    typer.echo(typer.style("🎉 Seeding complete!", typer.colors.GREEN, bold=True))
