from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from app.schemas.role_schema import RolePublic

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    adresse: str
    phone: str

class UserCreate(UserBase):
    password_hash: str
    role_ids: List[int]

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    adresse: Optional[str] = None
    phone: Optional[str] = None
    role_ids: Optional[List[int]] = None  # Pour pouvoir update les rôles

class UserPublic(UserBase):
    id: int
    roles: List[RolePublic]

    class Config:
        orm_mode = True