from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.models.user_role import Role


class UserBase(BaseModel):
    username: str = Field(None, max_length=50)
    email: EmailStr = Field(None, max_length=255)
    first_name: str = Field(None, max_length=50)
    last_name: str = Field(None, max_length=50)
    adresse: str = Field(None)
    phone: str = Field(None, max_length=30)
    roles: list[Role] | None


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50, nullable=False)
    email: EmailStr = Field(..., max_length=255, nullable=False)
    first_name: str = Field(..., max_length=50, nullable=False)
    last_name: str = Field(..., max_length=50, nullable=False)
    adresse: str = Field(...)
    phone: str = Field(..., max_length=30)
    roles: list[int]
    password_hash: str = Field(..., nullable=False)


class UserUpdate(UserBase):
    pass


class UserPublic(UserCreate):
    id: int
