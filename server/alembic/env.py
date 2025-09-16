from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# make project package importable (so `from db import Base` works when alembic
# is executed from the `server/` directory)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# If the DATABASE_URL environment variable isn't set (for example when
# running `alembic` directly), prefer the value from alembic.ini. We must
# set this environment variable before importing `db` because `db.py`
# creates an Engine at import time using that variable.
db_url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if db_url:
    os.environ["DATABASE_URL"] = db_url

# import your MetaData for 'autogenerate' support after DATABASE_URL is set
from db import Base
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
    # prefer DATABASE_URL environment variable if provided
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        config.set_main_option("sqlalchemy.url", db_url)

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # allow DATABASE_URL env var to override the ini file
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        config.set_main_option("sqlalchemy.url", db_url)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
