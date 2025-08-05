from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "ADMIN"
    employee = "EMPLOYEE"
    customer = "CUSTOMER"

class Role(SQLModel, table=True):
    id: Optional[int] = Field(..., primary_key=True)
    role: str = Field(..., unique=True, nullable=False, ) # RoleEnum