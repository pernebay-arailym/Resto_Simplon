from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from enum import Enum
from .user_role_link import UserRoleLink


class RoleType(str, Enum):
    admin = "admin"
    employee = "employee"
    customer = "customer"


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role_type: RoleType = Field(unique=True)
    users: List["User"] = Relationship(
        back_populates="roles", link_model=UserRoleLink
    )
