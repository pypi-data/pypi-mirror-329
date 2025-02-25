import os
from pathlib import Path
import typer

from ..choice.startproject import StartProjectChoice
from ..function.startproject import create_and_activate_env, create_file

from ..template.startproject import get_api_contant, get_console_content, get_database_contant, get_env_file_content, get_gitignore_contant, get_helper_utilities_content, get_loging_contant, get_manage_contant, get_server_contant, get_urls_contant, get_welcome_controller_contant
from .basic import app


def create_folder_structure(base_dir: str):
    """Creates the folder and file structure."""
    folders = [
        "app/commands",
        "app/helpers",
        "app/http/v1/controllers",
        "app/http/v1/responses",
        "app/http/v1/validators",
        "app/middleware",
        "app/models",
        "app/services",
        "config",
        "database/migrations",
        "database/seeders",
        "routes",
        "storage/logs",
        "tests"
    ]

    files = {
        f"{base_dir}/app/commands/__init__.py": "",
        f"{base_dir}/app/config.py": "# Configuration file",
        f"{base_dir}/app/http/v1/urls.py": "# all routes file\n"+get_urls_contant(),
        f"{base_dir}/app/helpers/__init__.py": "",
        f"{base_dir}/app/helpers/utils.py": "# Utility functions"+get_helper_utilities_content(),
        f"{base_dir}/app/http/v1/controllers/__init__.py": "",
        f"{base_dir}/app/http/v1/controllers/welcome_controller.py": "#Welcome Controller  "+get_welcome_controller_contant(),
        f"{base_dir}/app/http/v1/responses/__init__.py": "",
        f"{base_dir}/app/http/v1/validators/__init__.py": "",
        f"{base_dir}/app/middleware/__init__.py": "",
        f"{base_dir}/app/models/__init__.py": "",
        f"{base_dir}/app/services/__init__.py": "",
        f"{base_dir}/config/__init__.py": "",
        f"{base_dir}/config/database.py": "# Database Configuration\n"+get_database_contant(),
        f"{base_dir}/config/logging.py": "# Logging Configuration\n"+get_loging_contant(),
        f"{base_dir}/config/settings.py": "# Settings Configuration",
        f"{base_dir}/database/__init__.py": "",
        f"{base_dir}/database/run_seeders.py": "# Run Seeders",
        f"{base_dir}/database/seeders/__init__.py": "",
        f"{base_dir}/routes/api.py": "# API Routes\n"+get_api_contant(),
        f"{base_dir}/routes/channel.py": "# Channel Routes",
        f"{base_dir}/routes/console.py": "# Console Routes\n"+get_console_content(),
        f"{base_dir}/server.py": "# Entry point\n"+get_server_contant(),
        f"{base_dir}/manage.py": "# Entry point\n"+get_manage_contant(),
        f"{base_dir}/storage/logs/app.log": "",
        f"{base_dir}/storage/logs/error.log": "",
        f"{base_dir}/tests/__init__.py": "",
        f"{base_dir}/README.md": "# Project Readme",
        f"{base_dir}/.env": "# Project Envirment variable"+get_env_file_content(),
        f"{base_dir}/.env.example": "# Project Envirment varialble"+get_env_file_content(),
        f"{base_dir}/Dockerfile": "# Dockerfile",
        f"{base_dir}/.gitignore": get_gitignore_contant(),
        f"{base_dir}/docker-compose.yml": "# Docker Compose Configuration",
    }

    # Create folders
    for folder in folders:
        os.makedirs(f"{base_dir}/{folder}", exist_ok=True)

    # Create files
    for file, content in files.items():
        create_file(file, content)
    
@app.command("startproject")
def startproject(name: str):
    """Create a new project structure."""

    base_dir = Path(name).resolve()
    os.makedirs(base_dir, exist_ok=True)
    create_folder_structure(str(base_dir))
    create_and_activate_env(base_dir)
    StartProjectChoice.dependency_management_choose()
    StartProjectChoice.choose_database()
    StartProjectChoice.add_alembic()
    typer.echo(typer.style(f"Project '{name}' created successfully at {base_dir}!",typer.colors.GREEN,bold=True))




