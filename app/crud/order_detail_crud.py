from typing import List, Optional
from app.models.order_detail import OrderDetail
from app.schemas.order_detail_schema import (
    OrderDetailCreate,
    OrderDetailUpdate,
)
from sqlmodel import Session, select


def create_order_detail(
    session: Session, order_detail: OrderDetailCreate
) -> OrderDetail:
    """
    Create a new order detail in the databas
    Args:
        session (Session): The database session.
        order detail (OrderDetailCreate): The order detail data to create.
    Returns:
        Order detail: The created order detail.
    """
    db_order_detail = OrderDetail.model_validate(order_detail)
    session.add(db_order_detail)
    session.commit()
    session.refresh(db_order_detail)
    return db_order_detail


def get_order_detail(
    session: Session, order_detail_id: int
) -> Optional[OrderDetail]:
    """
    Retrieve an order detail by ID from the database.
    Args:
        session (Session): The database session.
        order_detail_id (int): The ID of the order detail to retrieve.
    Returns:
        Order detail: The order detail object if found,
          otherwise raises ValueError.
    """
    db_order_detail = session.get(OrderDetail, order_detail_id)
    if not db_order_detail:
        return None
    return db_order_detail


def get_all_order_details(session: Session) -> list[OrderDetail]:
    """
    Retrieve all order details from the database.
    Args:
        session (Session): The database session.
    Returns:
        list[Order detail]: A list of all order detail objects.
    """
    statement = select(OrderDetail)
    return list(session.exec(statement).all())


def update_order_detail(
    session: Session,
    order_detail_id: int,
    order_detail_update: OrderDetailUpdate,
) -> Optional[OrderDetail]:
    """
    Update an existing order detail in the database.
    Args:
        session (Session): The database session.
        order_detail_update (OrderDetailUpdate): The updated order detail data.
    Returns:
        Order detail: The updated order detail object.
    """
    db_order_detail = session.get(OrderDetail, order_detail_id)
    if not db_order_detail:
        return None

    order_detail_data = order_detail_update.model_dump(exclude_unset=True)
    for key, value in order_detail_data.items():
        setattr(db_order_detail, key, value)

    session.add(db_order_detail)
    session.commit()
    session.refresh(db_order_detail)
    return db_order_detail


def delete_order_detail(session: Session, order_detail_id: int) -> None:
    """
    Delete an order detail from the database.
    Args:
        session (Session): The database session.
        order_detail_id (int): The ID of the order detail to delete.
    Raises:
        ValueError: If the order detail with the given ID does not exist.
    """
    db_order_detail = session.get(OrderDetail, order_detail_id)
    if not db_order_detail:
        return None

    session.delete(db_order_detail)
    session.commit()


def get_all_order_details_by_order(
    session: Session, order_id: int
) -> List[OrderDetail]:
    """
    Retrieve all order details of an order from the database.
    Args:
        session (Session): The database session.
    Returns:
        list[Order detail]: A list of all order details objects from an order.
    """
    statement = select(OrderDetail).where(OrderDetail.order_id == order_id)
    return list(session.exec(statement).all())
