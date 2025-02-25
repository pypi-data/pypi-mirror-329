import typer
from ..template.cli_content import get_test_case_content, get_views_content, get_model_contant, get_validator_content, get_servie_content, get_route_content
from ..function.check_class import check_class
from ..function.check_app import check_app

def make_views(name: str, app_name: str ):
 
    # Directory paths
    app_dir = check_app(app_name=app_name)
    controllers_dir = app_dir / "views"

    # Verify if the app exists

    # Capitalize the controller name and generate file name
    class_name = f"{name.capitalize()}View"
    file_name = f"{name.lower()}_view.py"
    file_path = controllers_dir / file_name

    # Check if the controller file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Controller boilerplate content
    content = get_views_content(name=name)

    # Ensure the controllers directory exists
    controllers_dir.mkdir(parents=True, exist_ok=True)

    # Write the controller file
    file_path.write_text(content)
    typer.echo(f"View '{class_name}' created successfully in '{file_path}'!")


def make_model(name: str, app_name: str):

    app_dir = check_app(app_name=app_name)
    models_dir = app_dir / "models"
    # Capitalize the model name and generate file name
    class_name = f"{name.capitalize()}Model"
    file_name = f"{name.lower()}_model.py"
    file_path = models_dir / file_name

    # Check if the model file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Model boilerplate content
    content = get_model_contant(name=name,app_name=app_name)

    # Ensure the models directory exists
    models_dir.mkdir(parents=True, exist_ok=True)

    # Write the model file
    file_path.write_text(content)
    typer.echo(f"Model '{class_name}' created successfully in '{file_path}'!")

def make_schema(name: str, app_name: str):
    # Directory paths
    app_dir = check_app(app_name=app_name)
    validators_dir = app_dir / "schemas"

    # Capitalize the validator name and generate file name
    class_name = f"{name.capitalize()}Schema"
    file_name = f"{name.lower()}_schema.py"
    file_path = validators_dir / file_name

    # Check if the validator file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Validator boilerplate content
    content = get_validator_content(name=name)  # noqa: F405
    # Ensure the validators directory exists
    validators_dir.mkdir(parents=True, exist_ok=True)

    # Write the validator file
    file_path.write_text(content)
    typer.echo(f"Schema '{class_name}' created successfully in '{file_path}'!")

def make_service(name: str, app_name: str):
   
    # Directory paths
    app_dir = check_app(app_name=app_name)

    services_dir = app_dir / "services"
    # Capitalize the service name and generate file name
    class_name = f"{name.capitalize()}Service"
    file_name = f"{name.lower()}_service.py"
    file_path = services_dir / file_name

    # Check if the service file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Service boilerplate content

    # Ensure the services directory exists
    services_dir.mkdir(parents=True, exist_ok=True)
    content = get_servie_content(name=name)
    # Write the service file
    file_path.write_text(content)
    typer.echo(f"Service '{class_name}' created successfully in '{file_path}'!")


def make_routes(name: str, app_name: str, routes: list):

    # Directory paths
    routes_folder = "http/v1"
    app_dir = check_app(app_name)
    routes_dir = app_dir / routes_folder

    # Capitalize the controller name and generate the file name
    controller_name = f"{name.capitalize()}Controller"
    file_name = "urls.py"
    file_path = routes_dir / file_name

    # Check if the route file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=controller_name)

    # Generate route content
    route_content = ""
    for method, route in routes:
        route_content += get_route_content(controller_name=controller_name, method=method, route_name=route) + "\n"

    # Ensure the routes directory exists
    routes_dir.mkdir(parents=True, exist_ok=True)

    # Write the route file
    file_path.write_text(f"""{route_content}""")

    typer.echo(f"Routes for '{controller_name}' created successfully in '{file_path}'!")
  
def make_tests(name: str, app_name: str):
   
    # Directory paths
    app_dir = check_app(app_name=app_name)

    services_dir = app_dir / "tests"
    # Capitalize the service name and generate file name
    class_name = f"{name.capitalize()}Test"
    file_name = f"{name.lower()}_test.py"
    file_path = services_dir / file_name

    # Check if the service file already exists
    check_class(file_path=file_path, app_name=app_name, class_name=class_name)

    # Service boilerplate content

    # Ensure the services directory exists
    services_dir.mkdir(parents=True, exist_ok=True)
    content = get_test_case_content(name=name)
    # Write the service file
    file_path.write_text(content)
    typer.echo(f"Service '{class_name}' created successfully in '{file_path}'!")

