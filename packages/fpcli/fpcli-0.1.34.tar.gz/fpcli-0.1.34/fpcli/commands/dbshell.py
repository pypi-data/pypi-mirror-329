from click import echo
import typer
import subprocess
import os
from .basic import app
from fpcli.function.get_settings import get_settings



@app.command("dbshell")
def dbshell():
    
    
    settings=get_settings()
    # Hardcoded database settings (Replace with actual values or environment variables)
    DB_ENGINE="postgresql"
    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD 
    DB_HOST = settings.DB_HOST 
    DB_NAME = settings.DB_NAME 
    """Open the database shell."""
    if DB_ENGINE == "postgresql":
        try:
            cmd = [
                "psql",
                "-h", DB_HOST,
                "-U", DB_USER,
                "-d", DB_NAME,
            ]
            env = os.environ.copy()
            env["PGPASSWORD"] = DB_PASSWORD  # Avoid password prompt
            typer.echo(f"Opening PostgreSQL shell for {DB_NAME}...")
            subprocess.run(cmd, env=env)
        except:
            typer.echo("You don't postgresql client -> sudo apt install postgresql-client ")

    elif DB_ENGINE in ["mysql", "mariadb"]:
        try:
            cmd = [
                "mysql",
                "-h", DB_HOST,
                "-u", DB_USER,
                f"--password={DB_PASSWORD}",
                DB_NAME,
            ]
            typer.echo(f"Opening MySQL shell for {DB_NAME}...")
            subprocess.run(cmd)
        except:
            typer.echo("You don't postgresql client -> sudo apt install postgresql-client ")


    else:
        typer.echo("Unsupported database engine.", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
