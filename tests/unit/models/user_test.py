import pytest
from datetime import datetime
from app.models.user import User


@pytest.fixture()
def user_data() -> dict:
    return {
        "id": 1,
        "username": "alexishs",
        "email": "alexis@example.com",
        "password_hash": "jhbububuvhtfryfihinhftdetsdriyfubiuijuhutftedytvubiuhihutgry",
        "created_at": datetime(2025, 9, 18, 15, 2, 58, 0),
        "first_name": "Alexis",
        "last_name": "Halbot-Schoonaert",
        "adresse": "123 rue du Paradis, 59000 LILLE",
        "phone": "0605040302",
    }


def test_user(user_data: dict):
    user = User(**user_data)
    assert user.id == 1
    assert user.username == "alexishs"
    assert (
        user.password_hash
        == "jhbububuvhtfryfihinhftdetsdriyfubiuijuhutftedytvubiuhihutgry"
    )
    assert user.email == "alexis@example.com"
    assert user.created_at == datetime(2025, 9, 18, 15, 2, 58, 0)
    assert user.first_name == "Alexis"
    assert user.last_name == "Halbot-Schoonaert"
    assert user.adresse == "123 rue du Paradis, 59000 LILLE"
    assert user.phone == "0605040302"
