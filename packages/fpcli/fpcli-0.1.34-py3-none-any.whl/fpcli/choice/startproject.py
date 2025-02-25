import typer
import subprocess

from ..function.startproject import  write_append_file

from ..template.startproject import get_config_setting_content, get_database_env_content

class StartProjectChoice:
    database_choice:int=0
    dependency_manager_choice:int=0

    @staticmethod
    def dependency_management_choose():
        """
        Choose between uv, poetry, or None, and install the selected one.
        """
        typer.echo("Select a dependency manager to install:")
        typer.echo("1. uv")
        typer.echo("2. poetry")
        typer.echo("3. None (Do not install any manager)")
        
        dependency_manager_choice = typer.prompt("Enter the number of your choice", type=int)
        StartProjectChoice.dependency_manager_choice=dependency_manager_choice

        if dependency_manager_choice == 1:
            typer.echo("You selected uv.")
            try:
                typer.echo("Installing uv...")
                try:
                    subprocess.run(["pip", "install", "uv"], check=True)
                except Exception :
                    subprocess.run(["pipx", "install", "uv"], check=True)

                subprocess.run(['uv','init'])
                subprocess.run(['uv','add', 'fastapi', 'uvicorn', 'fpcli'])
                typer.echo("uv installed successfully.")
            except subprocess.CalledProcessError:
                typer.echo("Failed to install uv. Please check your pip installation.")
        elif dependency_manager_choice == 2:
            typer.echo("You selected poetry.")
            try:
                typer.echo("Installing poetry...")
                try:
                    subprocess.run(["pip", "install", "poetry"], check=True)
                except Exception:
                    subprocess.run(["pipx", "install", "poetry"], check=True)

                subprocess.run(['poetry','init'])
                subprocess.run(['poetry','add', 'fastapi', 'uvicorn', 'fpcli'])

                typer.echo("poetry installed successfully.")
            except subprocess.CalledProcessError:
                typer.echo("Failed to install poetry. Please check your pip installation.")
        elif dependency_manager_choice == 3:
            typer.echo("You selected None. No dependency manager will be installed.")
        else:
            typer.echo("Invalid choice. Please run the command again and select a valid option.")
            raise typer.Exit()

    @staticmethod
    def choose_database():
        DATABASES = {
            "SQLite": ["sqlmodel","pydantic_settings"],
            "PostgreSQL": ["sqlmodel", "asyncpg", "databases","pydantic_settings"],
            "MySQL": ["sqlmodel", "mysqlclient", "databases","pydantic_settings"],
            "MongoDB": ["motor"]
        }

        if(StartProjectChoice.dependency_manager_choice!=3):
            typer.echo(typer.style("Please select a database from the list below:",typer.colors.WHITE,blink=True,bg=typer.colors.BLUE, bold=True))
            for idx, db in enumerate(DATABASES, start=1):
                typer.echo(typer.style(f"{idx}. {db}",bold=True))
            
            database_choice = typer.prompt("Enter the number of your choice", type=int)

            if 1 <= database_choice <= len(DATABASES) :
             
                
                selected_db:str = list(DATABASES.keys())[database_choice-1]


                if(StartProjectChoice.dependency_manager_choice==1):
                    DATABASES[selected_db].insert(0,"uv") # this menas installing the package for the uv
                elif(StartProjectChoice.dependency_manager_choice==2):
                    DATABASES[selected_db].insert(0,"poetry") # Thsi means installing the package for the poetry
            
                database_contant=get_database_env_content() 
                setting_config_contant=get_config_setting_content() 
                print(setting_config_contant)
                write_append_file(".env", database_contant[selected_db.lower()])
                write_append_file(".env.example", database_contant[selected_db.lower()])
                write_append_file("config/settings.py",setting_config_contant[selected_db.lower()])
                
                DATABASES[selected_db].insert(1,"add")
                subprocess.run(DATABASES[selected_db])
                typer.echo(f"You have selected: {selected_db}")
            else:
                typer.echo("Invalid choice. Please run the command again and choose a valid option.")
        
    def add_alembic():
        """
        Ask the user explicitly if they want to add Alembic for database migrations.
        Provides explicit 'yes' or 'no' options.
        """
        confirm = typer.prompt("Do you want to add Alembic for database migrations? (yes/no)", type=str, default="yes")
        
        if confirm.lower() in ["yes", "y"]:
            subprocess.run(['pip','install','alembic'])
            subprocess.run(['alembic','init','database/migrations'])
        
        elif confirm.lower() in ["no", "n"]:
            typer.echo("Skipped: Alembic will not be added.")
        else:
            typer.echo("Invalid option. Please enter 'yes' or 'no'.")

