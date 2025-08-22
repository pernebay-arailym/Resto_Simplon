from datetime import datetime, timezone
from app.models.order import OrderBase, OrderStatus


def test_instantiate_order():
    # Arrange
    input_data = {
        "client_id": 123,
        "total_price": 45.50,
        "status": OrderStatus.CREATED,
    }

    # Act
    order = OrderBase(**input_data)

    # Assert
    assert order.client_id == 123
    assert order.total_price == 45.50
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.created_at, datetime)
    assert order.created_at.tzinfo == timezone.utc
    assert order.id is None  # id should be None until persisted in DB
