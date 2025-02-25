from pathlib import Path
import typer
import os
import sys
import importlib.util
from fpcli.function import check_app
from .basic import app
from ..fpcli_settings import APP_FOLDER

@app.command("dbseed")
def dbseed(app_name: str, reset: bool = typer.Option(False, "--reset", help="Clear database before seeding")):
    """Run all seeders from scratch. Optionally reset the database before seeding."""

    check_app(app_name)
    SEEDER_FOLDER: Path = Path(f"{APP_FOLDER}/{app_name}/seeders").resolve()

    if not SEEDER_FOLDER.exists():
        typer.echo(typer.style("😥 No seeders found. Create them first!", typer.colors.YELLOW, bold=True))
        raise typer.Exit(1)

    # **1️⃣ Add the project root to sys.path**
    ROOT_DIR = str(Path(APP_FOLDER).resolve())
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)

    # Reset database if needed
    if reset:
        typer.echo(typer.style("🔄 Resetting database...", typer.colors.CYAN, bold=True))
        os.system(f"python {APP_FOLDER}/{app_name}/manage.py flush --noinput")  # Modify based on ORM
        typer.echo(typer.style("✅ Database reset complete.", typer.colors.GREEN, bold=True))

    # **2️⃣ Run seeders dynamically**
    file_lists = sorted(os.listdir(SEEDER_FOLDER))  # Ensure execution order
    for file in file_lists:
        if file.endswith(".py") and not file.startswith("__"):  # Ignore __init__.py
            seeder_path = SEEDER_FOLDER / file
            module_name = f"{app_name}.seeders.{file[:-3]}"  # Construct module name

            typer.echo(typer.style(f"🌱 Running {module_name}...", typer.colors.BLUE, bold=True))

            try:
                spec = importlib.util.spec_from_file_location(module_name, seeder_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # **3️⃣ Find the class dynamically**
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and hasattr(attr, "run") and callable(getattr(attr, "run")):
                        typer.echo(typer.style(f"🚀 Executing {attr_name}.run()...", typer.colors.MAGENTA, bold=True))
                        attr.run()  # Call the static run method

            except ModuleNotFoundError as e:
                typer.echo(typer.style(f"❌ Import error: {e}", typer.colors.RED, bold=True))
                typer.echo(typer.style(f"⚠️  Check if your seeder files use absolute imports!", typer.colors.YELLOW, bold=True))

    typer.echo(typer.style("🎉 Seeding complete!", typer.colors.GREEN, bold=True))

    # **4️⃣ Cleanup sys.path**
    if ROOT_DIR in sys.path:
        sys.path.remove(ROOT_DIR)
