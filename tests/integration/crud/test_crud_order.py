from fastapi.testclient import TestClient
import pytest
import uuid # for generating unique user emails 
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

from app.schemas.order_schema import OrderCreate
from app.crud.user_crud import delete_user
from app.models.user import User  # assuming you have a User model


@pytest.fixture
def sample_user(session):
    user = User(
        username="testuser",
        email=f"test_{uuid.uuid4().hex}@example.com",  # unique each run
        password_hash="hashedpassword",  # some dummy hash
        first_name="Test",
        last_name="User",
        adresse="123 Test Street",
        phone="1234567890",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_order(session, sample_user):
    order_data = OrderCreate(
        client_id=sample_user.id, total_price=100.0, status=OrderStatus.CREATED
    )
    order = create_order(session, order_data)       
    return order


# @pytest.fixture
# def sample_order(session):
# """Insert a sample order into the DB."""
# order_data = OrderCreate(client_id=1, total_price=100.0, status=OrderStatus.CREATED)
# order = create_order(session, order_data)
# return order


# Tests


def test_create_and_get_order(session: Session, sample_user):
    order_data = OrderCreate(
        client_id=sample_user.id,  # use the fixture user id
        total_price=50.0,
        status=OrderStatus.CREATED
    )
    order = create_order(session, order_data)

    assert order.id is not None
    assert order.client_id == sample_user.id
    assert order.total_price == 50.0
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.created_at, datetime)
    assert order.created_at.tzinfo in (None, timezone.utc)

    fetched = get_order(session, order.id)
    assert fetched.id == order.id
    assert fetched.client_id == sample_user.id
    delete_order(session, order.id)
    delete_user(session, sample_user.id)
      # Clean up the user after test    

#def test_get_all_orders(session: Session, sample_order):
    #orders = get_all_orders(session)
    #assert len(orders) >= 1
   # assert orders[0].id == sample_order.id
def test_get_all_orders(session: Session, sample_order):
    orders = get_all_orders(session)
    assert sample_order in orders
    user_id = sample_order.client_id
    delete_order(session, sample_order.id)
    delete_user(session, user_id)


def test_get_order_by_client_id(session: Session, sample_order):
    order = get_order_by_client_id(session, sample_order.client_id)
    assert order.id == sample_order.id
    assert order.client_id == sample_order.client_id
    user_id = sample_order.client_id
    delete_order(session, sample_order.id)
    delete_user(session, user_id)



def test_get_orders_by_date(session: Session, sample_order):
    today = date.today()
    orders = get_orders_by_date(session, today)
    assert sample_order in orders
    user_id = sample_order.client_id
    delete_order(session, sample_order.id)
    delete_user(session, user_id)
    #assert len(orders) >= 1
    #assert orders[0].id == sample_order.id


def test_update_order(session: Session, sample_order):
    update_data = OrderUpdate(total_price=200.0, status=OrderStatus.PREPARING)
    updated = update_order(session, sample_order.id, update_data)

    assert updated.total_price == 200.0
    assert updated.status == OrderStatus.PREPARING
    user_id = sample_order.client_id
    delete_order(session, sample_order.id)
    delete_user(session, user_id)



def test_delete_order(session: Session, sample_order):
    delete_order(session, sample_order.id)
    deleted = get_order(session, sample_order.id)
    assert deleted is None
    user_id = sample_order.client_id
    delete_user(session, user_id)
