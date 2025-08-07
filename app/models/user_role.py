from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
import sqlalchemy as sa
from datetime import datetime, timezone
from pydantic import EmailStr


class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(..., foreign_key="user.id", primary_key=True)
    role_id: int = Field(..., foreign_key="role.id", primary_key=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=50, nullable=False)
    email: EmailStr = Field(..., unique=True, max_length=255)
    password_hash: str = Field(...)
    created_at: datetime = Field(
        ..., default_factory=lambda: datetime.now(timezone.utc)
    )
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    adresse: str = Field(...)
    phone: str = Field(..., max_length=30)
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)


class RoleType(str, Enum):
    admin = "ADMIN"
    employee = "EMPLOYEE"
    customer = "CUSTOMER"


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO: Pourquoi il est impossible de mettre unique=True si on utilise un type énuméré ?
    role_type: RoleType = Field(
        ...,
        # unique=True,
        sa_column=sa.Column(sa.Enum(RoleType, name="role_type", create_type=True)),
    )  # RoleEnum
    users: list[User] = Relationship(back_populates="roles", link_model=UserRoleLink)
