from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import EmailStr
from .user_role_link import UserRoleLink


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, nullable=False)
    email: EmailStr = Field(..., unique=True, max_length=255)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    adresse: str = Field(nullable=False)
    phone: str = Field(max_length=30, nullable=False)
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)
