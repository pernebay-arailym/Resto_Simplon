# app/models/user_role.py
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from enum import Enum
import sqlalchemy as sa
from typing import Optional, List
from datetime import datetime, timezone

class RoleType(str, Enum):
    admin = "admin"
    employee = "employee"
    customer = "customer"

class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role_type: RoleType = Field(
        sa_column=sa.Column(
            sa.Enum(RoleType, name="role_type_enum"),
            unique=True,
            nullable=False,
        )
    )
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, nullable=False)
    email: EmailStr = Field(..., unique=True, max_length=255)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    adresse: str = Field(nullable=False)
    phone: str = Field(max_length=30, nullable=False)
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)
