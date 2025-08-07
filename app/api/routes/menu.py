from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.menu_schema import MenuCreate, MenuPublic, MenuUpdate
from app.crud import menu_crud
from typing import List

router = APIRouter(tags=["Menus"])


@router.post("/", response_model=MenuPublic)
def create_menu(*, session: SessionDep, menu_in: MenuCreate):
    """
    Create a new menu.

    Args:
        session (SessionDep): The database session dependency.
        menu_in (MenuCreate): The menu creation data.

    Raises:
        HTTPException: If the menu with this title already exists.
        HTTPException: If the menu creation fails.

    Returns:
        MenuPublic: The created menu data.
    """

    menu = menu_crud.get_menu_by_name(session=session, name=menu_in.name)
    if menu:
        raise HTTPException(
            status_code=400,
            detail="The menu with this name already exists in the system.",
        )

    menu = menu_crud.create_menu(session=session, menu=menu_in)

    return menu


@router.get("/", response_model=List[MenuPublic])
def get_all_menus(*, session: SessionDep):
    """
    Get all menus.

    Args:
        session (SessionDep): The database session dependency.
        menu_id (int): The ID of the menu to retrieve.

    Raises:
        HTTPException: If the menu is not found.

    Returns:
        MenuPublic: The retrieved menu data.
    """
    return menu_crud.get_all_menus(session=session)


@router.get("/{menu_id}", response_model=MenuPublic)
def get_menu_by_id(*, session: SessionDep, menu_id: int):
    """
    Get a menu by ID.

    Args:
        session (SessionDep): The database session dependency.
        menu_id (int): The ID of the menu to retrieve.

    Raises:
        HTTPException: If the menu is not found.

    Returns:
        MenuPublic: The retrieved menu data.
    """
    menu = menu_crud.get_menu_by_id(session=session, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    return menu


@router.put("/{menu_id}", response_model=dict)
def update_menu(*, session: SessionDep, menu_id: int, menu_in: MenuUpdate):
    """
    Update a menu by ID.

    Args:
        session (SessionDep): The database session dependency.
        menu_id (int): The ID of the menu to update.
        menu_in (MenuCreate): The menu update data.

    Raises:
        HTTPException: If the menu is not found.
        HTTPException: If the menu update fails.

    Returns:
        MenuPublic: The updated menu data.
    """

    menu = menu_crud.get_menu_by_id(session=session, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    updated_menu = menu_crud.update_menu(
        session=session, menu_id=menu_id, menu_update=menu_in
    )

    return updated_menu


@router.delete("/{menu_id}", response_model=dict)
def delete_menu(*, session: SessionDep, menu_id: int):
    """
    Delete a menu by ID.

    Args:
        session (SessionDep): The database session dependency.
        menu_id (int): The ID of the menu to delete.

    Raises:
        HTTPException: If the menu is not found.

    Returns:
        dict: A success message.
    """

    menu = menu_crud.get_menu_by_id(session=session, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    menu_crud.delete_menu(session=session, menu_id=menu_id)

    return {"detail": "Menu deleted successfully"}
