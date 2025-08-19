from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Menu(SQLModel, table=True):
    """
    Menu model.

    Args:
        SQLModel (SQLModel): Base class for SQLAlchemy models.
        table (bool, optional): Whether the model is a SQLAlchemy table. Defaults to False.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100, nullable=False, unique=True)
    price: float = Field(default=0, ge=0, nullable=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    description: str = Field(..., max_length=255)
    stock: int = Field(default=0, ge=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
