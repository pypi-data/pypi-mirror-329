from contextlib import asynccontextmanager
from typing import Annotated

from commons.db import DatabaseMigrationExecutor, DatabaseAdapter
from commons.db.cache import Cache
from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute

from webserver.config import settings


def generate_unique_route_id(route: APIRoute) -> str:
    """
    Generate a unique ID for the client side generation.
    Source: https://fastapi.tiangolo.com/advanced/generate-clients/#custom-operation-ids-and-better-method-names
    :return: route id
    """
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"{route.name}"

@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    """Manages the lifespan of a FastAPI application."""
    from sqlmodel import SQLModel, inspect
    from commons import runtime

    # --- FastAPI app startup
    # Load modules to allow orm metadada creation
    runtime.import_modules(settings.MODULES)

    # Create DB and Tables via ORM
    if settings.has_database:
        SQLModel.metadata.create_all(settings.database_adapter.engine())

        # create only the cache table on cache db
        if not inspect(settings.cache_database_adapter.engine()).has_table("cache"):
            runtime.import_module("commons.db.cache")
            SQLModel.metadata.tables["cache"].create(settings.cache_database_adapter.engine())

        # Migrate SQL Data
        with settings.database_adapter.session() as s:
            DatabaseMigrationExecutor(path=settings.resources_folder / "migrations", session=s).run()
            s.close()

    # --- FastAPI app execution
    yield
    # --- FastAPI app shutdown

# Sets a session as dependency
ServerDatabase = Annotated[DatabaseAdapter, Depends(lambda: settings.database_adapter)]
ServerCache = Annotated[Cache, Depends(lambda: Cache(database=settings.cache_database_adapter))]
