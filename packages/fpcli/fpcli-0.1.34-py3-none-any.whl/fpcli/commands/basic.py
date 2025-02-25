
from pathlib import Path
import typer
from ..template.cli_content import *
from ..fpcli_settings import CONFIG_FOLDER
import socket
import typer


app= typer.Typer()


@app.command("runserver")
def run_server(
    mode: str = typer.Option(
        "dev", 
        help="Run mode: 'dev' for development or 'prod' for production",
        case_sensitive=False
    ),
    host: str = typer.Option("127.0.0.1", help="The host to bind the server to"),
    port: int = typer.Option(8000, help="The port to run the server on"),
    workers: int = typer.Option(1, help="Number of worker processes for the server"),
):
    """
    Run the FastAPI server in development ('dev') or production ('prod') mode with a specified number of workers.
    """
    def is_port_in_use(host: str, port: int) -> bool:
        """Check if the given port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return False
            except socket.error:
                return True

    def find_available_port(host: str, port: int) -> int:
        """Find the next available port."""
        while is_port_in_use(host, port):
            port += 1
        return port

    try:
        import uvicorn

        if mode.lower() not in ["dev", "prod"]:
            typer.echo("Invalid mode. Use 'dev' for development or 'prod' for production.", err=True)
            raise typer.Exit(code=1)

        reload = mode.lower() == "dev"
        environment = "Development" if reload else "Production"

        # Check if port is in use, if so, find an available one
        port = find_available_port(host, port)

        typer.echo(f"Starting server in {environment} mode at http://{host}:{port} with {workers} workers...")
        uvicorn.run(f"{CONFIG_FOLDER}.main:app", host=host, port=port, reload=reload, workers=workers)
        print(f"🎉 Server started. at http://{host}:{port}")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


