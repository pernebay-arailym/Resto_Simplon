from typing import List
from app.models.order import OrderBase
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.models.order import OrderStatus
from app.models.order_detail import OrderDetailStatus
from app.crud.order_detail_crud import get_all_order_details_by_order
from sqlmodel import Session, select
from datetime import date, datetime, time


def create_order(session: Session, order: OrderCreate) -> OrderBase:
    """
    Create a new order in the databas
    Args:
        session (Session): The database session.
        order (OrderCreate): The order data to create.
    Returns:
        Order: The created order.
    """
    db_order = OrderBase.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


def get_order(session: Session, order_id: int) -> OrderBase:
    """
    Retrieve an order by ID from the database.
    Args:
        session (Session): The database session.
        order_id (int): The ID of the order to retrieve.
    Returns:
        Order: The order object if found, otherwise raises ValueError.
    """
    db_order = session.get(OrderBase, order_id)
    if not db_order:
        return None
    return db_order


def get_all_orders(session: Session) -> List[OrderBase]:
    """
    Retrieve all orders from the database.
    Args:
        session (Session): The database session.
    Returns:
        list[Order]: A list of all order objects.
    """
    statement = select(OrderBase)
    return session.exec(statement).all()


def get_order_by_client_id(session: Session, client_id: int) -> OrderBase:
    """
    Retrieve a order by its title from the database.
    Args:
        session (Session): The database session.
        client_id(int): The client_id of the order to retrieve.
    Returns:
        Order: The order object if found, otherwise raises ValueError.
    """
    statement = select(OrderBase).where(OrderBase.client_id == client_id)
    db_order = session.exec(
        statement
    ).first()  # TODO we get only the first order with the client_id
    return db_order


def get_orders_by_date(session: Session, target_date: date) -> List[OrderBase]:
    """
    Retrieve all orders by their date from the database.
    Args:
        session (Session): The database session.
        target_date(date): The date of the orders to retrieve.
    Returns:
        List[Order]: The order object if found, otherwise raises ValueError.
    """
    start_date = datetime.combine(target_date, time.min)
    end_date = datetime.combine(target_date, time.max)
    statement = select(OrderBase).where(
        OrderBase.created_at.between(start_date, end_date)
    )
    return session.exec(statement).all()


def update_order(
    session: Session, order_id: int, order_update: OrderUpdate
) -> OrderBase:
    """
    Update an existing order in the database.
    Args:
        session (Session): The database session.
        order_update (OrderUpdate): The updated order data.
    Returns:
        Order: The updated order object.
    """
    db_order = session.get(OrderBase, order_id)
    if not db_order:
        return None

    order_data = order_update.model_dump(exclude_unset=True)
    for key, value in order_data.items():
        setattr(db_order, key, value)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


def delete_order(session: Session, order_id: int) -> None:
    """
    Delete an order from the database.
    Args:
        session (Session): The database session.
        order_id (int): The ID of the order to delete.
    Raises:
        ValueError: If the order with the given ID does not exist.
    """
    db_order = session.get(OrderBase, order_id)
    if not db_order:
        return None

    session.delete(db_order)
    session.commit()


def get_order_total(session: Session, order_id: int) -> float:
    """
    Compute the order total price.
    Args:
        session (Session): The database session.
        order_id (int): The ID of the order.
    Raises:
        ValueError: If the order with the given ID does not exist.
    Returns:
        float: The total price of the order.
    """
    # order = get_order(session, order_id)
    order_details = get_all_order_details_by_order(session, order_id)
    order_total = 0
    for order_detail in order_details:
        if order_detail.status is not OrderDetailStatus.CANCELLED:
            order_total += order_detail.price * order_detail.quantity
    return float(order_total)


def finalize_order(session: Session, order_id: int) -> OrderBase:
    """
    Finalize an order.
    Args:
        session (Session): The database session.
        order_id (int): The ID of the order to delete.
    Raises:
        ValueError: If the order with the given ID does not exist.
    Returns:
        OrderBase: The updated order object.
    """
    order = get_order(session, order_id)
    # Finalize can only be made if the order is in status "created"
    if order.status is OrderStatus.CREATED:
        order_update = OrderUpdate(
            client_id=order.client_id,
            status=OrderStatus.PREPARING,
            total_price=get_order_total(session, order_id),
        )
        update_order(session, order_id, order_update)
        order = get_order(session, order_id)
    return order
