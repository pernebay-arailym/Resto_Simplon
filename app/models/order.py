from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Literal
from typing import Optional
from enum import Enum


class OrderStatus(str, Enum):  # Enum for order status to ensure valid values.
    CREATED = "Created"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"
    PAID = "Paid"


class OrderBase(
    SQLModel, table=True
):  # Order model representing a customer's order in the restaurant system.

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(..., foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(default=OrderStatus.CREATED)  # Using the OrderStatus enum for status field
