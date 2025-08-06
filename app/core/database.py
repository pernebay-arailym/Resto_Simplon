from sqlmodel import Session, create_engine
from app.models.user_role import UserRoleLink, User, Role
from app.core.config import settings

# L'engine de la base de données
engine = create_engine(str(settings.DATABASE_URL), echo=True)

def create_db_and_tables():
    """
    Crée les tables de la base de données si elles n'existent pas.
    """
    # SQLModel.metadata.create_all(engine)
    # Il est souvent préférable d'utiliser des migrations comme Alembic pour un projet en production.
    pass

def get_session():
    """
    Dépendance pour obtenir une session de base de données.
    """
    with Session(engine) as session:
        yield session