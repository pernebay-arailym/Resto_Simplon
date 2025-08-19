import pytest
from typing import List
from sqlmodel import Session
from app.core.database import engine
from app.schemas.user_schema import UserCreate
from app.crud import user_crud
from tests import conftest


@pytest.fixture()
def user_data() -> dict:
    return {
        "id": 42,
        "username": "alexishs",
        "email": "alexis@example.com",
        "first_name": "Alexis",
        "last_name": "Halbot-Schoonaert",
        "adresse": "123 rue du Paradis, 59000 LILLE",
        "phone": "0605040302",
        "password_hash": "khbhiobgviyviuvtvutvyctxeyrtvuvuobubytvdctexdt",
        "role_ids": [1],
    }


def test_create_user(session: Session, user_data: dict):
    try:
        # user_schema = UserCreate(**user_data)
        user_schema = UserCreate(
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            adresse=user_data["adresse"],
            phone=user_data["phone"],
            password_hash=user_data["password_hash"],
            role_ids=user_data["role_ids"],
        )
        user = user_crud.create_user(session, user_schema)
        conftest.compare_object_to_dict(user, user_data, ["id", "password_hash"])
    finally:
        user_crud.delete_user(session, user.id)
