from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    adresse: str = Field(...)
    phone: str = Field(..., max_length=30)


class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=8)
    role_ids: List[int] = Field(..., min_items=1)


class UserPublicCreate(UserBase):
    password_hash: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=255)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    adresse: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=30)
    role_ids: Optional[List[int]] = Field(None)


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password_hash: str = Field(...)


class UserPublic(UserBase):
    id: int

    class Config:
        orm_mode = True
