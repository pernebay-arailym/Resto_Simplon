from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """
    Category creation model that can be used for creating new categories.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    name: str = Field(..., max_length=100)


class CategoryUpdate(BaseModel):
    """
    Category update model that can be used for updating existing categories.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    name: str = Field(None, max_length=100)


class CategoryPublic(CategoryCreate):
    """
    Public representation of a category.

    Args:
        CategoryCreate (CategoryCreate): Base model for category creation.
    """

    id: int
    name: str
