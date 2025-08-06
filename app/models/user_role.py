from __future__ import annotations
from sqlmodel import Field, SQLModel


class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(..., foreign_key="user.id", primary_key=True)
    role_id: int = Field(..., foreign_key="role.id", primary_key=True)
