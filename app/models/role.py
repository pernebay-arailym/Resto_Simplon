from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa


class RoleType(str, Enum):
    admin = "ADMIN"
    employee = "EMPLOYEE"
    customer = "CUSTOMER"


class Role(SQLModel, table=True):
    id: Optional[int] = Field(..., primary_key=True)
    role_type: str = Field(
        ...,
        unique=True,
        nullable=False,
        sa_column=sa.Column(sa.Enum(RoleType, name="role_type", create_type=True)),
    )  # RoleEnum
