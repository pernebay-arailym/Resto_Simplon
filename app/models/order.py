from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Literal
from typing import Optional
from enum import Enum
import sqlalchemy as sa

# On commence par le modèle OrderBase.
# C’est la représentation d’une commande dans notre base de données.


class OrderStatus(str, Enum):  # Enum for order status to ensure valid values.
    CREATED = "Created"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"
    PAID = "Paid"


# Il contient l’ID, l’ID du client, la date de création, le prix total et le statut.


class OrderBase(
    SQLModel, table=True
):  # Order model representing a customer's order in the restaurant system.
    __tablename__ = "order"
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(..., foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_price: float = Field(..., gt=0)
    status: OrderStatus = Field(...)


# Le statut est limité grâce à une énumération OrderStatus, ce qui évite d’avoir des valeurs incorrectes.
# En résumé, ce modèle est la base : il définit comment une commande existe dans notre système.
