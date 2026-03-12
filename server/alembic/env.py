"""
Alembic environment configuration.
"""

import os
import sys
from logging.config import fileConfig
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy import create_engine

# -------------------------------------------------------------------
# Path Configuration
# -------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# -------------------------------------------------------------------
# App Imports
# -------------------------------------------------------------------

from app.core.config import settings
from app.db.base import Base
from app.models.conversation import Conversation, AgentLog  # noqa: F401

# -------------------------------------------------------------------
# Alembic Config
# -------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use sync DB URL for Alembic (remove asyncpg driver)
db_url = settings.DATABASE_URL
if "+asyncpg" in db_url:
    db_url = db_url.replace("+asyncpg", "")
# Replace postgresql+asyncpg:// with postgresql://
if "postgresql+asyncpg://" in db_url:
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata

# -------------------------------------------------------------------
# Offline Migrations
# -------------------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------------------------
# Online Migrations
# -------------------------------------------------------------------


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------------------
# Migration Runner
# -------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
