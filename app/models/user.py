from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from app.models.role import Role
from app.models.user_role import UserRoleLink

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=50, nullable=False)
    email: EmailStr = Field(..., unique=True, max_length=255)
    password_hash: str = Field(...)
    created_at: datetime = Field(..., default_factory=lambda: datetime.now(timezone.utc))
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    adresse: str = Field(...)
    phone: str = Field(..., max_length=30)
    role: list["Role"] = Relationship(
        back_populates="user",
        link_model="UserRoleLink"
    )