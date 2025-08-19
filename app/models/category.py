from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Category(SQLModel, table=True):
    """
    Category model.

    Args:
        SQLModel (SQLModel): Base class for SQLAlchemy models.
        table (bool, optional): Whether the model is a SQLAlchemy table. Defaults to False.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100, nullable=False, unique=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
