from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(
        (
            f'postgresql+asyncpg://'
            f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
            f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}'
            f'/{settings.POSTGRES_DB}'
        ),
        pool_size=20,
        pool_pre_ping=True,
        pool_use_lifo=True,
    )
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def _setup_cache(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the cache.

    This function creates Redis client instance
    and stores it in the application's state property.

    :param app: fastAPI application.
    """
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
    app.state.redis_client = redis_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    _setup_db(app)
    _setup_cache(app)
    yield
    await app.state.db_engine.dispose()
    await app.state.redis_client.aclose()