from app.models.category import Category


def test_instantiate_category():
    # Arrange
    input_data = {"name": "desserts"}

    # Act
    category = Category(name=input_data["name"])

    # Assert
    assert category.name == "desserts"
