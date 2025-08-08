from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, timezone
from app.models.order import OrderStatus

# Les schémas servent à définir la forme exacte des données que notre API accepte ou renvoie.


class OrderCreate(BaseModel):
    """
    Order creation model that can be used for creating new orders.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    client_id: int = Field(...)
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(...)  # Using the OrderStatus enum for status field


class OrderUpdate(BaseModel):
    """
    Order update model that can be used for updating existing orders.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    client_id: int = Field(None)
    total_price: float = Field(None, gt=0)
    status: OrderStatus = Field(None)


class OrderPublic(OrderCreate):
    """
    Public representation of a order.

    Args:
        OrderCreate (OrderCreate): Base model for order creation.
    """

    client_id: int
    total_price: float
    status: OrderStatus

    class Config:
        orm_mode = True


# Ces schémas sont comme des “contrats” : ils garantissent que les données respectent un format précis, ce qui rend l’API plus fiable.
