from pydantic import BaseModel, Field
import sqlalchemy as sa
from app.models.user_role import RoleType


class RoleBase(BaseModel):
    role_type: RoleType = Field(
        ..., sa_column=sa.Column(sa.Enum(RoleType, name="role_type", create_type=True))
    )  # Using the RoleType enum for status field


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RolePublic(RoleBase):
    id: int
