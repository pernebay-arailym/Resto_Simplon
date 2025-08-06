from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    """
    Menu creation model that can be used for creating new menus.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    name: str = Field(..., max_length=100)
    price: float = Field(default=0, ge=0)
    category_id: int = Field(...)
    description: str = Field(..., max_length=255)
    stock: int = Field(default=0, ge=0)


class MenuUpdate(BaseModel):
    """
    Menu update model that can be used for updating existing menus.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    name: str = Field(None, max_length=100)
    price: float = Field(None, ge=0)
    category_id: int = Field(None)
    description: str = Field(None, max_length=255)
    stock: int = Field(None, ge=0)


class MenuPublic(MenuCreate):
    """
    Public representation of a menu.

    Args:
        MenuCreate (MenuCreate): Base model for menu creation.
    """

    id: int
    name: str
