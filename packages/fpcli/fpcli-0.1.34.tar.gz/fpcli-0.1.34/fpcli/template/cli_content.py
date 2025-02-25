from pydoc import classname


def get_views_content(name: str):
    class_name = f"{name.capitalize()}View"
    return f'''
from fastapi import Request

class {class_name}:

    async def index(self):
        """Get all the data"""
        
        return " Get all the data."

    async def create(self, request: Request):
        """Create new data based on the request."""
        return f"Create new data based on the request."


    async def edit(self, uuid: str):
        """Read or edit the data based on the given UUID. """
        
        return "Read or edit the data based on the given UUID. "

    async def update(self, request: Request, uuid: str):
        """Update the data based on the given UUID."""
        
        return f"fUpdate the data based on the given UUID."

    async def destroy(self, uuid: str):
        """ Delete the data based on the given UUID."""
        
        return "for delete the data"
        '''


def get_model_contant(name: str, app_name: str = None):
    class_name = f"{name.capitalize()}Model"
    return f'''
from typing import Optional
from sqlmodel import SQLModel,Field
from datetime import datetime


class {class_name}(SQLModel,table=True):
    """
    {class_name} represents the schema for {app_name.lower()}_{name.lower()}.
    """
    __tablename__ = '{app_name.lower()}_{name.lower()}'

    id: int= Field(default=None, primary_key=True)
    name: str
    status: Optional[bool] = Field(True, description="Last update timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(default=None, description="Deletion timestamp")
    
    '''


def get_validator_content(name: str):
    class_name = f"{name.capitalize()}Schema"
    return f'''
from pydantic import BaseModel, Field
from typing import Optional

class {class_name}(BaseModel):
    """
    {class_name} is used to validate {name} data.
    """
    uuid: Optional[str] = Field(None, description="Unique identifier for the data")
    name: str = Field(..., description="Name field")
    '''


def get_servie_content(name: str):
    class_name = f"{name.capitalize()}Service"

    return f'''
from typing import List, Optional
from sqlmodel import select
from uuid import UUID
from ..models.{name.lower()}_model import {name.capitalize()}Model
from .. import db

class {name.capitalize()}Service:
    """
    {name.capitalize()}Service handles the business logic and database operations for {name}.
    """

    @staticmethod
    async def create(data: dict) -> {name.capitalize()}Model:
        """Create a new {name.capitalize()}. """
        async with db() as session:
            instance = {name.capitalize()}Model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @staticmethod
    async def get_all() -> List[{name.capitalize()}Model]:
        """Fetch all {name}s."""
        async with db() as session:
            result = await session.execute(select({name.capitalize()}Model))
            return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID) -> Optional[{name.capitalize()}Model]:
        """Fetch a {name} by its UUID."""
        async with db() as session:
            return await session.get({name.capitalize()}Model, uuid)

    @staticmethod
    async def update(uuid: UUID, data: dict) -> Optional[{name.capitalize()}Model]:
        """Update an existing {name}."""
        async with db() as session:
            instance = session.get({name.capitalize()}Model, uuid)
            if instance:
                for key, value in data.items():
                    setattr(instance, key, value)
                await session.commit()
                await session.refresh(instance)
            return instance

    @staticmethod
    async def delete(uuid: UUID) -> bool:
        """Delete a {name} by its UUID."""
        async with db() as session:
            instance = session.get({name.capitalize()}Model, uuid)
            if instance:
                await session.delete(instance)
                await session.commit()
                return True
            return False
    '''


def get_middleware_content(name: str):
    class_name = f"{name.capitalize()}Middleware"

    return f'''
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

class {class_name}(BaseHTTPMiddleware):
    """
    {class_name} is a custom middleware for processing requests and responses.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Intercept the incoming request, process it, then call the next handler.
        
        Args:
            request (Request): The incoming request.
            call_next (Callable): The function to call the next middleware or route handler.
        
        Returns:
            Response: The final response to be returned.
        """


        # Call the next middleware or route handler
        response = await call_next(request)


        return response
    '''


def get_seeder_content(name: str, app_name: str):
    class_name = f"{name.capitalize()}Seeder"
    service_name = f"{name.capitalize()}Service"
    return f'''
from ..services.{name.lower()}_service import {service_name}

class {class_name}:
    """
    Seeder for {name.capitalize()}Model to populate initial data.
    """

    @staticmethod
    async def run():
        """
        Run the seeder to insert sample data into the database.
        """
        records = [
            {{
                "name": "{name.capitalize()}1",
               
            }},
            {{
                "name": "{name.capitalize()}2",

            }}
        ]

        # Insert the data into the database using a loop
        for record in records:
            await {service_name}.create(record)

        print(f"{class_name} seed successfully!")
    '''


def get_route_content(controller_name: str, method: str, route_name: str):
    """
    Generate FastAPI route snippet in the format of app_router.add_api_route.

    Args:
        controller_name (str): The name of the controller (e.g., UserController).
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.).
        route_name (str): The route name (e.g., '/user/', '/user/create').

    Returns:
        str: The generated route snippet in the desired format.
    """
    # Extract the controller method name dynamically
    controller_method = route_name.strip("/").replace("/", "_")

    # Generate the route content in app_router.add_api_route format
    return f'app_router.add_api_route("{route_name}", {controller_name}().{controller_method}, methods={["{method}"]})'


def get_test_case_content(name: str):
    from ..fpcli_settings import CONFIG_FOLDER

    return f"""
from fastapi.testclient import TestClient
from {CONFIG_FOLDER.lower()}.main import app  

client = TestClient(app)

async def test_list_{name}(self):
    response = client.get("/{name}s")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_create_{name}(self):
    response = client.post("/{name}s", json={{"name": "test"}})
    assert response.status_code == 201
    assert response.json()["name"] == "test"

async def test_get_{name}(self):
    response = client.get("/{name}s/1")
    assert response.status_code == 200
    assert response.json()["name"] == "test"

async def test_update_{name}(self):
    response = client.put("/{name}s/1", json={{"name": "updated"}})
    assert response.status_code == 200
    assert response.json()["name"] == "updated"

async def test_delete_{name}(self):
    response = client.delete("/{name}s/1")
    assert response.status_code == 200"""
