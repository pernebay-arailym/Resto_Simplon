import pytest
from typing import List
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.core.database import engine


@pytest.fixture()
def session():
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


def compare_object_to_dict(
    an_object: any,
    a_dict: dict,
    properties_to_exclude: List[str] | None = None,
) -> bool:
    if an_object is None:
        assert False, "Object is None"
    else:
        if properties_to_exclude is None:
            properties_to_exclude = []
        for property in dir(an_object):
            if (property in a_dict.keys()) and (
                property not in properties_to_exclude
            ):
                if getattr(an_object, property) != a_dict[property]:
                    print(
                        f"Property {property} should equal {a_dict[property]} but equals {getattr(an_object, property)}"
                    )
                    assert (
                        False
                    ), f"Property {property} should equal {a_dict[property]} but equals {getattr(an_object, property)}"
