import typer
import subprocess
import os
from ..fpcli_settings import APP_FOLDER
from .basic import app

APPS_DIR = APP_FOLDER   # Adjust this path as needed

def discover_test_modules():
    """Discover test modules in FastAPI apps."""
    test_modules = []
    for app_name in os.listdir(APPS_DIR):
        test_dir = os.path.join(APPS_DIR, app_name, "tests")  # Adjusted to 'tests' instead of 'tests'
        if os.path.exists(test_dir):
            test_modules.append(test_dir)
    return test_modules

def run_fastapi_tests(app_name=None):
    """Run FastAPI tests using pytest for all test files in the 'test' folder."""
    test_dirs = [os.path.join(APPS_DIR, app_name, "test")] if app_name else discover_test_modules()
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            command = ["pytest", test_dir]
            typer.echo(typer.style(f"Running tests in {test_dir}............................................................................", fg=typer.colors.BRIGHT_YELLOW, bold=True))
            subprocess.run(command)

@app.command("test")
def test(app_name: str = typer.Argument(None, help="Name of the app to test (optional)")):
    """Run all tests or tests for a specific app."""
    run_fastapi_tests(app_name)