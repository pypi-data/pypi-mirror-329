import typer

from ..function.make_ai_test_case import test_file_processing
from ..template.cli_content import get_middleware_content, get_seeder_content
from ..function.check_class import check_class
from ..function.check_app import check_app
from ..function.basic import make_model, make_routes, make_schema, make_service, make_tests,  make_views

make=typer.Typer()



@make.command("make:view")
def view(name: str, app_name: str , 
               sc: bool=typer.Option(False,help=f"for Creating the Schema for data validation you can pass Sc. Sc mean { typer.style('Schema',typer.colors.YELLOW,bold=True) }   "),
               s: bool=typer.Option(False,help=f"for Creating the Service you can pass S. S mean  { typer.style('Service',typer.colors.GREEN,bold=True) } "),
               m: bool=typer.Option(False,help=f"for Creating the Model you can pass M. M mean Model { typer.style('Model',typer.colors.BRIGHT_RED,bold=True) } "),
               r: bool=typer.Option(False,help=f"for Creating the all Routes you can pass S. S mean  { typer.style('Resource',typer.colors.BRIGHT_BLUE,bold=True) } ")):
    
    """
    Generate a FastAPI controller file with a user-defined name inside a specific app.
    """
    if(m):
        print(m,s,r)

    make_views(name=name,app_name=app_name)
    if(m):
        make_model(name=name,app_name=app_name)
    if(s):
        make_service(name=name,app_name=app_name)
    if(sc):
        make_schema(name=name,app_name=app_name)
    if(r):
        make_routes(name=name,app_name=app_name)

@make.command("make:model")
def model(name: str, app_name: str , 
               sc: bool=typer.Option(False,help=f"for Creating the Schema for data validation you can pass Sc. Sc mean { typer.style('Schema',typer.colors.YELLOW,bold=True) }   "),
               s: bool=typer.Option(False,help=f"for Creating the Service you can pass S. S mean  { typer.style('Service',typer.colors.GREEN,bold=True) } "),
               v: bool=typer.Option(False,help=f"for Creating the View you can pass V. V means  { typer.style('View',typer.colors.YELLOW,bold=True) } "),
               r: bool=typer.Option(False,help=f"for Creating the all Routes you can pass S. S mean  { typer.style('Resource',typer.colors.BRIGHT_BLUE,bold=True) } ")):
    """
    Generate a Beanie ODM model file with a user-defined name inside a specific app.
    """
    
    make_model(name=name,app_name=app_name)
    if(v):
        make_views(name=name,app_name=app_name)
    if(s):
        make_service(name=name,app_name=app_name)
    if(sc):
        make_schema(name=name,app_name=app_name)
    if(r):
        make_routes(name=name,app_name=app_name)



@make.command("make:schema")
def schema(name: str, app_name: str , 
               v: bool=typer.Option(False,help=f"for Creating the Views you can pass v. v means { typer.style('View',typer.colors.BRIGHT_YELLOW,bold=True) } "),
               s: bool=typer.Option(False,help=f"for Creating the Service you can pass S. S mean  { typer.style('Service',typer.colors.YELLOW,bold=True) } "),
               m: bool=typer.Option(False,help=f"for Creating the Model you can pass M. M mean Model { typer.style('Service',typer.colors.BRIGHT_RED,bold=True) } "),
               r: bool=typer.Option(False,help=f"for Creating the all Routes you can pass r. r mean  { typer.style('Resource',typer.colors.BRIGHT_RED,bold=True) } ")):
    """
    Generate a Pydantic validator file with a user-defined name inside a specific app.
    """
    make_schema(name=name,app_name=app_name)
    if(v):
        make_views(name=name,app_name=app_name)
    if(s):
        make_service(name=name,app_name=app_name)
    if(m):
        make_model(name=name,app_name=app_name)
    if(r):
        make_routes(name=name,app_name=app_name)

@make.command("make:service")
def service(name: str, app_name: str , 
               v: bool=typer.Option(False,help=f"for Creating the Validator you can pass S. S mean { typer.style('Validator',typer.colors.YELLOW,bold=True) }   "),
               m: bool=typer.Option(False,help=f"for Creating the Model you can pass M. M mean  { typer.style('Model',typer.colors.GREEN,bold=True) } "),
               sc: bool=typer.Option(False,help=f"for Creating the Schema for data validation you can pass Sc. Sc mean { typer.style('Schema',typer.colors.YELLOW,bold=True) }   "),
               r: bool=typer.Option(False,help=f"for Creating the all Routes you can pass S. S mean  { typer.style('Resource',typer.colors.BRIGHT_BLUE,bold=True) } ")):
    """
    Generate a service class file with a user-defined name inside a specific app.
    """
    make_service(name=name,app_name=app_name)
    if(v):
        make_views(name=name,app_name=app_name)
    if(m):
        make_model(name=name,app_name=app_name)
    if(sc):
        make_schema(name=name,app_name=app_name)
    if(r):
        make_routes(name=name,app_name=app_name)
        



@make.command("make:middleware")
def make_middleware(name: str,app_name:str):
    """
    Generate a middleware file with a user-defined name inside a specific app.
    """
    # Directory paths
    app_dir = check_app(app_name=app_name)
    middleware_folder = "middleware"

    middleware_dir = app_dir / middleware_folder

    # Capitalize the middleware name and generate file name
    class_name = f"{name.capitalize()}Middleware"
    file_name = f"{name.lower()}_middleware.py"
    file_path = middleware_dir / file_name

    # Check if the middleware file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Middleware boilerplate content
    content = get_middleware_content(name=name)

    # Ensure the middleware directory exists
    middleware_dir.mkdir(parents=True, exist_ok=True)

    # Write the middleware file
    file_path.write_text(content)
    typer.echo(f"Middleware '{class_name}' created successfully in '{file_path}'!")


@make.command("make:seeder")
def make_seeder(name: str,app_name:str):
    """
    Generate a seeder file with a user-defined name inside a specific app.
    """
    # Directory paths
    app_dir = check_app(app_name=app_name)
    middleware_dir = app_dir / "seeders"

    # Capitalize the seeder name and generate file name
    class_name = f"{name.capitalize()}Seeder"
    file_name = f"{name.lower()}_seeder.py"
    file_path = middleware_dir / file_name

    # Check if the seeder file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Middleware boilerplate content
    content = get_seeder_content(name=name,app_name=app_name)

    # Ensure the seeder directory exists
    middleware_dir.mkdir(parents=True, exist_ok=True)

    # Write the seeder file
    file_path.write_text(content)
    typer.echo(f"Seeder '{class_name}' created successfully in '{file_path}'!")


   
@make.command("make:routes")
def create_routes(name: str, app_name: str, routes: str):
    """
    Generate route file with user-defined routes inside a specific app.
    Routes should be passed as a  string.
    Example: 'GET,POST,PUT'
    """
    # make_routes(name, app_name, routes)
    

@make.command("make:test")
def make_test(name: str, app_name: str , 
               v: bool=typer.Option(False,help=f"for Creating the Validator you can pass V. V mean { typer.style('Validator',typer.colors.YELLOW,bold=True) }   "),
               s: bool=typer.Option(False,help=f"for Creating the Validator you can pass S. S mean { typer.style('Service',typer.colors.BRIGHT_MAGENTA,bold=True) }   "),
               m: bool=typer.Option(False,help=f"for Creating the Model you can pass M. M mean  { typer.style('Model',typer.colors.GREEN,bold=True) } "),
               sc: bool=typer.Option(False,help=f"for Creating the Schema for data validation you can pass Sc. Sc mean { typer.style('Schema',typer.colors.YELLOW,bold=True) }   "),
               r: bool=typer.Option(False,help=f"for Creating the all Routes you can pass S. S mean  { typer.style('Resource',typer.colors.BRIGHT_BLUE,bold=True) } "),
               ai: bool=typer.Option(False,help=f"If you passed the AI then automatically generate the test case file   { typer.style('Test file',typer.colors.BRIGHT_BLUE,bold=True) } ")):
    """
    Generate a service class file with a user-defined name inside a specific app.
    """
    if(ai):
        test_file_processing(app_name=app_name,keyword=name)
    else:
        make_tests(name=name,app_name=app_name)
    if(s):
        make_service(name=name,app_name=app_name)
    if(v):
        make_views(name=name,app_name=app_name)
    if(m):
        make_model(name=name,app_name=app_name)
    if(sc):
        make_schema(name=name,app_name=app_name)
    if(r):
        make_routes(name=name,app_name=app_name)

