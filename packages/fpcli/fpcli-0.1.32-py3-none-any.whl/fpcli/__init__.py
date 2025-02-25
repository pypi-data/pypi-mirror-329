import typer
from .commands import app, make  # Ensure make is a Typer() instance in commands.py 

# app = typer.Typer()  # Initialize main Typer app

# Add grouped commands
app.add_typer(make, help="Make commands")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main entry point."""
    if ctx.invoked_subcommand is None:
        help_text = ctx.get_help()  # Get default help output
        typer.echo(help_text)  # Print default help
        typer.echo("\nAvailable Commands:\n")  # Append grouped commands
        raise typer.Exit()


if __name__ == "__main__":
    app()
