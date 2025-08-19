import pytest
from datetime import datetime, date, timezone
from sqlmodel import SQLModel, Session, create_engine
from app.models.order import OrderBase, OrderStatus
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.crud.order_crud import (
    create_order,
    get_order,
    get_all_orders,
    get_order_by_client_id,
    get_orders_by_date,
    update_order,
    delete_order,
)

DATABASE_URL = "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@psql_dev:5432/${POSTGRES_DB}"


@pytest.fixture(scope="session")
def engine():
    """Create a Postgres engine for the test session."""
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.drop_all(engine)  # clean slate
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Provide a fresh DB session for each test."""
    with Session(engine) as session:
        yield session
        session.rollback()  # rollback anything not committed


@pytest.fixture
def sample_order(session):
    """Insert a sample order into the DB."""
    order_data = OrderCreate(client_id=1, total_price=100.0, status=OrderStatus.CREATED)
    order = create_order(session, order_data)
    return order


# Tests


def test_create_and_get_order(session):
    order_data = OrderCreate(client_id=1, total_price=50.0, status=OrderStatus.CREATED)
    order = create_order(session, order_data)

    assert order.id is not None
    assert order.client_id == 1
    assert order.total_price == 50.0
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.created_at, datetime)
    assert order.created_at.tzinfo in (None, timezone.utc)

    fetched = get_order(session, order.id)
    assert fetched.id == order.id
    assert fetched.client_id == 1


def test_get_all_orders(session, sample_order):
    orders = get_all_orders(session)
    assert len(orders) >= 1
    assert orders[0].id == sample_order.id


def test_get_order_by_client_id(session, sample_order):
    order = get_order_by_client_id(session, sample_order.client_id)
    assert order.id == sample_order.id
    assert order.client_id == sample_order.client_id


def test_get_orders_by_date(session, sample_order):
    today = date.today()
    orders = get_orders_by_date(session, today)
    assert len(orders) >= 1
    assert orders[0].id == sample_order.id


def test_update_order(session, sample_order):
    update_data = OrderUpdate(total_price=200.0, status=OrderStatus.PREPARING)
    updated = update_order(session, sample_order.id, update_data)

    assert updated.total_price == 200.0
    assert updated.status == OrderStatus.PREPARING


def test_delete_order(session, sample_order):
    delete_order(session, sample_order.id)
    deleted = get_order(session, sample_order.id)
    assert deleted is None
