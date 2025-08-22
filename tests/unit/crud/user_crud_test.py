import pytest
from typing import List
from sqlmodel import Session
from app.core.database import engine
from app.models.role import RoleType
from app.schemas.user_schema import UserCreate
from app.schemas.role_schema import RoleCreate
from app.crud import user_crud, role_crud
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
        role_1 = role_crud.get_role_by_id(session, 1)
        role_2 = role_crud.get_role_by_id(session, 2)
        role_3 = role_crud.get_role_by_id(session, 3)
        if (role_1 is None) or (role_2 is None) or (role_3 is None):
            role_1 = role_crud.create_role(
                session, RoleCreate(role_type=RoleType.admin)
            )
            role_2 = role_crud.create_role(
                session, RoleCreate(role_type=RoleType.employee)
            )
            role_3 = role_crud.create_role(
                session, RoleCreate(role_type=RoleType.customer)
            )
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
        conftest.compare_object_to_dict(
            user, user_data, ["id", "password_hash"]
        )
    finally:
        user_crud.delete_user(session, user.id)
