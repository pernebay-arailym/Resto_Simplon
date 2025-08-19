from pydantic import BaseModel, Field
from app.models.order_detail import OrderDetailStatus


class OrderDetailCreate(BaseModel):
    """
    Order detail creation model that can be used for creating new orders.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    order_id: int = Field(...)
    menu_id: int = Field(...)
    status: OrderDetailStatus = Field(...)
    price: float = Field(..., ge=0)
    comment: str = Field(default="", max_length=255)
    quantity: int = Field(..., gt=0)


class OrderDetailUpdate(BaseModel):
    """
    Order update model that can be used for updating existing orders.

    Args:
        BaseModel (BaseModel): Base model for Pydantic schemas.
    """

    order_id: int = Field(None)
    menu_id: int = Field(None)
    status: OrderDetailStatus = Field(None)
    price: float = Field(None, ge=0)
    comment: str = Field(None, max_length=255)
    quantity: int = Field(None, gt=0)


class OrderDetailPublic(OrderDetailCreate):
    """
    Public representation of a order detail.

    Args:
        OrderDetailCreate (OrderDetailCreate): Base model for order detail creation.
    """

    id: int
    order_id: int
    menu_id: int
    status: OrderDetailStatus
    price: float
    comment: str
    quantity: int

    class Config:
        orm_mode = True
