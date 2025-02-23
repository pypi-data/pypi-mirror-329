from contextlib import asynccontextmanager
from typing import Generator, Annotated

from commons.db import DatabaseMigrationExecutor
from commons.db.cache import Cache
from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from sqlmodel import Session

from webserver.config import settings


def get_db_session(**kwargs) -> Session:
    """
    Get a default database session
    :param kwargs:
    :return:
    """
    from webserver.config import settings
    return Session(settings.database_adapter.engine(), **kwargs)

def get_cache_db() -> Cache:
    """Get a cache database session"""
    from webserver.config import settings
    return Cache(database=settings.cache_database_adapter)

def _get_fastapi_database_session() -> Generator[Session]:
    s: Session = get_db_session()

    try:
        yield s
    finally:
        s.close()

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
    from sqlmodel import SQLModel
    from commons import runtime

    # --- FastAPI app startup
    # Load modules to allow orm metadada creation
    settings.MODULES.append("commons.db.cache")
    runtime.import_modules(settings.MODULES)

    # Create DB and Tables via ORM
    if settings.has_database:
        SQLModel.metadata.create_all(settings.database_adapter.engine())
        SQLModel.metadata.tables["cacheentry"].create(settings.cache_database_adapter.engine())

        # Migrate SQL Data
        with get_db_session() as s:
            DatabaseMigrationExecutor(path=settings.resources_folder / "migrations", session=s).run()
            s.close()

    # --- FastAPI app execution
    yield
    # --- FastAPI app shutdown

# Sets a session as dependency
ServerDatabaseSession = Annotated[Session, Depends(_get_fastapi_database_session)]
ServerCacheDatabase = Annotated[Session, Depends(get_cache_db)]
