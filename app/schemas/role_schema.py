from pydantic import BaseModel, Field
from app.models.user_role import RoleType


class RoleBase(BaseModel):
    role_type: RoleType = Field(...)  # Using the RoleType enum for status field


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class UserPublic(RoleBase):
    id: int
