from app.models.menu import Menu


def test_instantiate_menu():
    # Arrange
    input_data = {
        "name": "4 fromages",
        "price": 12.54,
        "category_id": 3,
        "description": "toukeskifo",
        "stock": 7,
    }

    # Act
    menu = Menu(**input_data)

    # Assert
    assert menu.name == "4 fromages"
    assert menu.price == 12.54
    assert menu.category_id == 3
    assert menu.description == "toukeskifo"
    assert menu.stock == 7
