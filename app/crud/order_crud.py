from app.models.order import OrderBase
from app.schemas.order_schema import OrderCreate, OrderUpdate
from sqlmodel import Session, select


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


def get_all_orders(session: Session) -> list[OrderBase]:
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
