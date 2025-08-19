from pydantic import BaseModel, Field
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    """
    Order creation model that can be used for creating new orders.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    client_id: int = Field(...)
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(
        ...
    )  # Using the OrderStatus enum for status field


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

    id: int
    client_id: int
    total_price: float
    status: OrderStatus

    class Config:
        orm_mode = True
