from pydantic import BaseModel
import sqlalchemy as sa
from app.models.role import RoleType


class RoleBase(BaseModel):
    role_type: RoleType


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RolePublic(RoleBase):
    id: int
