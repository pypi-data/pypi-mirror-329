import os
from pathlib import Path
import typer
from ..template.startapp import get_init_content
from ..function.check_app import is_exits
from ..function.startproject import create_file
from ..template.startproject import   get_helper_utilities_content,  get_urls_contant, get_welcome_controller_contant
from ..function.makeapp import makeapp_with_folder
from .basic import app
from ..fpcli_settings import APP_FOLDER

def create_folder_structure(base_dir: str):
    """Creates the folder and file structure."""
    folders = [
    ]

    files = {
        f"{base_dir}/__init__.py": "# Configuration file\n"+get_init_content(),
        f"{base_dir}/urls.py": "# all routes file\n"+get_urls_contant(),
        f"{base_dir}/utils.py": "# Utility functions \n\n"+get_helper_utilities_content(),
        f"{base_dir}/views.py": "#Welcome View  "+get_welcome_controller_contant(),
        f"{base_dir}/schemas.py": "",
        f"{base_dir}/test.py": "",
        f"{base_dir}/models.py": "",
    }

    # Create folders
    for folder in folders:
        os.makedirs(f"{base_dir}/{folder}", exist_ok=True)

    # Create files
    for file, content in files.items():
        create_file(file, content)
    
@app.command("startapp")
def startapp(app_name: str, nofolder: bool = typer.Option(False, help="Pass --nofolder to create a simple file-based app")):
    """Create a new APP Structure. --f to Create APP with Folder structure"""
    is_exits(app_name=app_name)
    base_dir = Path(f"{APP_FOLDER}/{app_name}").resolve()
    if nofolder:
        create_folder_structure(str(base_dir))
    else:
        makeapp_with_folder(base_dir)

    typer.echo(f"🎉 App '{app_name}' created successfully at {base_dir}!")

