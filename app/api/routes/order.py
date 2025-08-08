from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.order_schema import OrderCreate, OrderPublic, OrderUpdate
from app.crud import order_crud
from typing import List

router = APIRouter(tags=["Order"])


@router.post("/", response_model=OrderPublic)
def create_order(*, session: SessionDep, order_in: OrderCreate):
    """
    Create a new order.

    Args:
        session (SessionDep): The database session dependency.
        order_in (OrderCreate): The ordercreation data.

    Raises:
        HTTPException: If the order with this title already exists.
        HTTPException: If the order creation fails.

    Returns:
        OrderPublic: The created order data.
    """

    order = order_crud.create_order(session=session, order=order_in)

    return order


@router.get("/{order_id}", response_model=OrderPublic)
def get_order(*, session: SessionDep, order_id: int):
    """
    Get a order by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order to retrieve.

    Raises:
        HTTPException: If the order is not found.

    Returns:
        OrderPublic: The retrieved order data.
    """
    order = order_crud.get_order(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/", response_model=List[OrderPublic])
def get_all_orders(*, session: SessionDep):

    # Get all order.

    return order_crud.get_all_orders(session=session)


@router.put("/{order_id}", response_model=OrderPublic)
def update_order(*, session: SessionDep, order_id: int, order_in: OrderUpdate):
    """
    Update an order by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order to update.
        order_in (OrderCreate): The order update data.

    Raises:
        HTTPException: If the order is not found.
        HTTPException: If the order update fails.

    Returns:
        OrderPublic: The updated order data.
    """

    order = order_crud.get_order(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = order_crud.update_order(
        session=session, order_id=order_id, order_update=order_in
    )

    return updated_order


@router.delete("/{order_id}", response_model=dict)
def delete_order(*, session: SessionDep, order_id: int):
    """
    Delete an order by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order to delete.

    Raises:
        HTTPException: If the order is not found.

    Returns:
        dict: A success message.
    """

    order = order_crud.get_order(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_crud.delete_order(session=session, order_id=order_id)

    return {"detail": "Order deleted successfully"}
