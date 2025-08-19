import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from app.main import app

from pydantic_settings import BaseSettings
from app.core.database import engine
import os


# Récupération de l'URL de la base de données de test à partir des variables d'environnement
# C'est la ligne la plus importante. Vous devez vous assurer que cette variable est bien injectée.
TEST_DATABASE_URL = os.getenv("DATABASE_URL")

# Gère le cas où la variable n'est pas définie
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not set in environment variables.")


@pytest.fixture(name="session")
def session_fixture():
    """
    Fixture qui fournit une session de base de données pour chaque test.
    """
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client_test")
def client_test_fixture(session: Session):
    """
    Fixture qui crée un client de test FastAPI en utilisant la session de test.
    """

    client_test = TestClient(app)
    yield client_test

    app.dependency_overrides.clear()
