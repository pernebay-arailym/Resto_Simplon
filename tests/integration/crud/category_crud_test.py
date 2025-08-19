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
    name_test = "test"

    category = CategoryCreate(name=name_test)
    categ_ = create_category(session, category)

    # Vérifiez que l'élément a bien été créé en base de données
    categ = session.get(Category, categ_.id)
    assert categ.name == name_test
    assert categ.id is not None
    delete_category(session, categ.id)


def test_get_category_by_id(session: Session, sample_category):
    category = get_category_by_id(session, sample_category.id)
    assert category.name == "category_test"
    assert category.id == sample_category.id
    delete_category(session, sample_category.id)


def test_get_all_categories(session: Session, sample_category):
    categories = get_all_categories(session)
    assert len(categories) >= 1
    assert categories[len(categories) - 1].name == sample_category.name
    delete_category(session, sample_category.id)


def test_get_category_by_name(session: Session, sample_category):
    category = get_category_by_name(session, sample_category.name)
    assert category.name == "category_test"
    assert category.id == sample_category.id
    delete_category(session, sample_category.id)


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
