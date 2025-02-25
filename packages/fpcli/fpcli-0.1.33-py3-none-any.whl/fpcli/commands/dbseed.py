from pathlib import Path
import typer
import os
import sys
import importlib.util
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

    module_name = f"__init__.py"  # Construct module name

    typer.echo(
        typer.style(f"🌱 Running {module_name}...", typer.colors.BLUE, bold=True)
    )

    # try:
    spec = importlib.util.spec_from_file_location(
        module_name, SEEDER_FOLDER / "__init__.py"
    )
    print(spec)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # except ModuleNotFoundError as e:
    #     typer.echo(typer.style(f"❌ Import error: {e}", typer.colors.RED, bold=True))
    #     typer.echo(
    #         typer.style(
    #             f"⚠️  Check if your seeder files use absolute imports!",
    #             typer.colors.YELLOW,
    #             bold=True,
    #         )
    #     )

    typer.echo(typer.style("🎉 Seeding complete!", typer.colors.GREEN, bold=True))
