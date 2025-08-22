from app.models.order_detail import OrderDetail, OrderDetailStatus


def test_instantiate_order_detail():
    # Arrange
    input_data = {
        "order_id": 3,
        "menu_id": 2,
        "price": 12.10,
        "comment": "sans champi",
        "quantity": 3,
        "status": OrderDetailStatus.CREATED,
    }

    # Act
    order_detail = OrderDetail(**input_data)

    # Assert
    assert order_detail.order_id == 3
    assert order_detail.menu_id == 2
    assert order_detail.price == 12.10
    assert order_detail.comment == "sans champi"
    assert order_detail.quantity == 3
    assert order_detail.status == OrderDetailStatus.CREATED
