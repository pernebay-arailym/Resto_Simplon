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
    users: List["User"] = Relationship(  # type: ignore[name-defined]
        back_populates="roles", link_model=UserRoleLink
    )
    # # test de relation User <> Role sans table intermédiaire
    # user_id: int = Field(foreign_key="user.id", primary_key=True)
    # role_type: RoleType = Field(primary_key=True)
