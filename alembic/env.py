import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
import sqlmodel

from alembic import context

# Ajoutez ces imports pour charger le fichier .env
from dotenv import load_dotenv

# Chargez le fichier .env
load_dotenv()

# Ceci est le MetaData de SQLModel
from sqlmodel import SQLModel

# Ceci est l'endroit où vous importez vos modèles
# par exemple, si vos modèles sont dans un fichier "models.py" dans le répertoire "app"
from app.models.user import User
from app.models.user_role import UserRoleLink
from app.models.role import Role
from app.models.category import Category
from app.models.menu import Menu

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python's standard logging.
# This ensures that all loggers use the same configuration.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata est le MetaData que les migrations vont utiliser
target_metadata = SQLModel.metadata

naming_convention = {
    "ix": "ix_%(table_name)_%(column_0_label)s",
    "uq": "uq_%(table_name)_%(column_0_name)s",
    "ck": "ck_%(table_name)_%(constraint_name)s",
    "fk": "fk_%(table_name)_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)",
}


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        naming_convention=naming_convention,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Utilisez la variable d'environnement pour la chaîne de connexion
    connectable = create_engine(os.getenv("DATABASE_URL"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            naming_convention=naming_convention,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
