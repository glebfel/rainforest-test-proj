import asyncio
from logging.config import fileConfig

from sqlalchemy.future import Connection

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.settings import settings
from src.db.base import Base
from src.db.models.orders import OrderModel, OrderItemModel
from src.db.models.products import ProductModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=(f'postgresql+asyncpg://'
             f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
             f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}'
             f'/{settings.POSTGRES_DB}'),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run actual sync migrations.

    :param connection: connection to the database.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_async_engine(
        (f'postgresql+asyncpg://'
         f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
         f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}'
         f'/{settings.POSTGRES_DB}'),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    task = run_migrations_offline()
else:
    task = run_migrations_online()

asyncio.run(task)
