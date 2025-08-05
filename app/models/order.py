
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Literal
from typing import Optional
import uuid #A UUID is a 128-bit number used to uniquely identify information in computer systems.

class OrderBase(SQLModel, table=True): #Order model representing a customer's order in the restaurant system.
    

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: uuid.UUID = Field(..., foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_price: float = Field(..., gt=0)
    status: Literal["Created", "Preparing", "Ready", "Served", "Cancelled", "Paid"] = Field(...)