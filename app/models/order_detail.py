from sqlmodel import Field, SQLModel
from typing import Literal
from typing import Optional
from enum import Enum
import sqlalchemy as sa


class OrderDetailStatus(str, Enum):  # Enum for order status to ensure valid values.
    CREATED = "Created"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"


class OrderDetail(
    SQLModel, table=True
):  # OrderDetail links an Order to its MenuItems (many-to-many).

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    menu_id: int = Field(..., foreign_key="menu.id")
    price: float = Field(..., ge=0)
    comment: str = Field(default="", max_length=255)
    quantity: int = Field(..., gt=0)
    status: OrderDetailStatus = Field(...)
