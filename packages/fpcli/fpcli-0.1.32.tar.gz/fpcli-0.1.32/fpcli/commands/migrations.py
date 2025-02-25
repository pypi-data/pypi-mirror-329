import subprocess
import typer
from .basic import app
import datetime



@app.command("makemigrations")
def makemigrations(message: str = "Auto migration" ,     m: bool = typer.Option(False, "--migrate", help="Apply migrations after generating them"),
):
    """Generate Alembic migrations with timestamp and incremental file naming."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g., 20250130_143215
        full_message = f"{timestamp}_{message}"  # e.g., "20250130_143215_Add_student_table"

        typer.echo(f"🚀 Generating migration in {full_message} ...")

        subprocess.run(["alembic",  "revision", "--autogenerate", "-m", full_message], check=True)

        typer.echo("✅ Migration generated successfully.")

        if(m==True):
            migrate()

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Error running migration: {e}")

@app.command("migrate")
def migrate_to_database():
    """ Apply Alembic migrations ."""
    migrate()


def migrate():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)

        typer.echo("🎉 Migration applied successfully!")
    
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Error running migration: {e}")