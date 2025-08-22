from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.order_schema import OrderCreate, OrderPublic, OrderUpdate
from app.schemas.order_detail_schema import OrderDetailPublic
from app.crud import order_crud, order_detail_crud
from typing import List
from datetime import date

from fastapi import Depends
from app.auth.auth_bearer import (
    RoleChecker,
    TokenResponse,
    get_current_user_payload,
)
from app.models.role import RoleType

router = APIRouter(tags=["Order"])


@router.post(
    "/",
    response_model=OrderPublic,
    dependencies=[Depends(get_current_user_payload)],
)
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


@router.get(
    "/{order_id}",
    response_model=OrderPublic,
    dependencies=[Depends(get_current_user_payload)],
)
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


@router.get(
    "/",
    response_model=List[OrderPublic],
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_all_orders(*, session: SessionDep):

    # Get all order.

    return order_crud.get_all_orders(session=session)


@router.put(
    "/{order_id}",
    response_model=OrderPublic,
    dependencies=[Depends(get_current_user_payload)],
)
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


@router.delete(
    "/{order_id}",
    response_model=dict,
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
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


@router.get(
    "/by_date/{year}/{month}/{day}",
    response_model=List[OrderPublic],
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_all_orders_by_date(
    *, session: SessionDep, year: int, month: int, day: int
):
    """
    Get all orders by created_at date.

    Args:
        session (SessionDep): The database session dependency.
        year (int): Date Year.
        month (int): Date month.
        day (int): Date day.

    Raises:
        HTTPException: If no order is found.

    Returns:
        OrderPublic: The retrieved orders data.
    """
    target_date = date(year, month, day)
    return order_crud.get_orders_by_date(session, target_date)


@router.get(
    "/{order_id}/details",
    response_model=List[OrderDetailPublic],
    dependencies=[Depends(get_current_user_payload)],
)
def get_all_order_details_by_order(*, session: SessionDep, order_id: int):
    """
    Get all orders by created_at date.

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order to get details.

    Raises:
        HTTPException: If no order is found.

    Returns:
        OrderPublic: The retrieved orders data.
    """
    return order_detail_crud.get_all_order_details_by_order(session, order_id)


@router.get(
    "/{order_id}/order_total",
    response_model=float,
    dependencies=[Depends(get_current_user_payload)],
)
def get_order_total(*, session: SessionDep, order_id: int):
    """
    Get an order total price.

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order.

    Raises:
        HTTPException: If no order is found.

    Returns:
        float: The retrieved order total.
    """
    return order_crud.get_order_total(session, order_id)


@router.get(
    "/{order_id}/finalize_order",
    response_model=OrderPublic,
    dependencies=[Depends(get_current_user_payload)],
)
def get_finalize_order(*, session: SessionDep, order_id: int):
    """
    "Finalize" an order (after lines being added,
    computes the total price and set status to PREPARING).

    Args:
        session (SessionDep): The database session dependency.
        order_id (int): The ID of the order.

    Raises:
        HTTPException: If no order is found.

    Returns:
        OrderPublic: The updated order.
    """
    return order_crud.finalize_order(session, order_id)
