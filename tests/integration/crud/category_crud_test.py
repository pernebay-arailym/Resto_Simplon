from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session
from app.models.category import Category
from app.crud.category_crud import (
    create_category,
    delete_category,
    get_category_by_id,
    get_all_categories,
    get_category_by_name,
    update_category,
)
from app.schemas.category_schema import CategoryCreate


@pytest.fixture
def sample_category(session):
    """Insert a sample category into the DB."""
    category_data = CategoryCreate(name="category_test")
    category = create_category(session, category_data)
    return category


def test_create_category(session: Session):
    """
    Tests the creation of a category.
    """
    detest = "test"
    # response = client_test.post("/api/v1/categories/", json={"name": detest})

    category = CategoryCreate(name=detest)
    categ_ = create_category(session, category)

    # assert response.status_code == 200

    # data = response.json()

    # Vérifiez que l'élément a bien été créé en base de données
    categ = session.get(Category, categ_.id)
    assert categ.name == detest
    assert categ.id is not None

    delete_category(session, categ.id)

    # cat = session.get(Category, categ.id)
    # assert cat is not None
    # assert category.name == detest


def test_get_category_by_id(session: Session):
    pass


def test_get_all_categories(session: Session):
    pass


def test_get_category_by_name():
    pass


def test_update_category():
    pass


def test_delete_category(session: Session):
    """
    Tests the delete of a category.
    """
    detest = "delete_test"
    # response = client_test.post("/api/v1/categories/", json={"name": detest})

    category = CategoryCreate(name=detest)
    categ_ = create_category(session, category)

    # assert response.status_code == 200

    # data = response.json()

    # Vérifiez que l'élément a bien été créé en base de données
    categ = session.get(Category, categ_.id)

    delete_category(session, categ.id)

    categ = session.get(Category, categ_.id)

    assert categ is None
