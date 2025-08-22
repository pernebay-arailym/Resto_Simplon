from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.order_detail_schema import (
    OrderDetailCreate,
    OrderDetailPublic,
    OrderDetailUpdate,
)
from app.crud import order_detail_crud
from typing import List

from fastapi import Depends
from app.auth.auth_bearer import (
    RoleChecker,
    TokenResponse,
    get_current_user_payload,
)
from app.models.role import RoleType

router = APIRouter(tags=["Order Detail"])


@router.post(
    "/",
    response_model=OrderDetailPublic,
    dependencies=[Depends(get_current_user_payload)],
)
def create_order_detail(
    *, session: SessionDep, order_detail_in: OrderDetailCreate
):
    """
    Create a new order detail.

    Args:
        session (SessionDep): The database session dependency.
        order_detail_in (OrderDetailCreate): The orderdetailcreation data.

    Raises:
        HTTPException: If the order_detail with this title already exists.
        HTTPException: If the order_detail creation fails.

    Returns:
        OrderPublic: The created order detail data.
    """
    order_detail = order_detail_crud.create_order_detail(
        session=session, order_detail=order_detail_in
    )

    return order_detail


@router.get(
    "/{order_detail_id}",
    response_model=OrderDetailPublic,
    dependencies=[Depends(get_current_user_payload)],
)
def get_order_detail(*, session: SessionDep, order_detail_id: int):
    """
    Get a order detail by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_detail_id (int): The ID of the order detail to retrieve.

    Raises:
        HTTPException: If the order detail is not found.

    Returns:
        OrderDetailPublic: The retrieved order_detail data.
    """
    order_detail = order_detail_crud.get_order_detail(
        session=session, order_detail_id=order_detail_id
    )
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")

    return order_detail


@router.get(
    "/",
    response_model=List[OrderDetailPublic],
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_all_order_details(*, session: SessionDep):

    # Get all order details.

    return order_detail_crud.get_all_order_details(session=session)


@router.put(
    "/{order_detail_id}",
    response_model=dict,
    dependencies=[Depends(get_current_user_payload)],
)
def update_order_detail(
    *,
    session: SessionDep,
    order_detail_id: int,
    order_detail_in: OrderDetailUpdate,
):
    """
    Update an order detail by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_detail_id (uuid.int): The ID of the order detail to update.
        order_detail_in (OrderDetailCreate): The order update data.

    Raises:
        HTTPException: If the order_detail is not found.
        HTTPException: If the order_detail update fails.

    Returns:
        OrderPublic: The updated order detail data.
    """

    order_detail = order_detail_crud.get_order_detail(
        session=session, order_detail_id=order_detail_id
    )
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")

    updated_order_detail = order_detail_crud.update_order_detail(
        session=session,
        order_detail_id=order_detail_id,
        order_detail_update=order_detail_in,
    )

    return updated_order_detail


@router.delete(
    "/{order_detail_id}",
    response_model=dict,
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def delete_order_detail(*, session: SessionDep, order_detail_id: int):
    """
    Delete an order detail by ID.

    Args:
        session (SessionDep): The database session dependency.
        order_detail_id (int): The ID of the order detail to delete.

    Raises:
        HTTPException: If the order detail is not found.

    Returns:
        dict: A success message.
    """

    order_detail = order_detail_crud.get_order_detail(
        session=session, order_detail_id=order_detail_id
    )
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")

    order_detail_crud.delete_order_detail(
        session=session, order_detail_id=order_detail_id
    )

    return {"detail": "Order Detail deleted successfully"}
