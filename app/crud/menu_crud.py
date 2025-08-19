from app.schemas.menu_schema import MenuCreate, MenuUpdate
from app.models.menu import Menu
from sqlmodel import Session, select


def create_menu(session: Session, menu: MenuCreate) -> Menu:
    """
    Create a new menu in the database.
    Args:
        session (Session): The database session.
        menu (MenuCreate): The menu data to create.
    Returns:
        Menu: The created menu.
    """
    db_menu = Menu.model_validate(menu)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


def get_menu_by_id(session: Session, menu_id: int) -> Menu:
    """
    Retrieve a menu by ID from the database.
    Args:
        session (Session): The database session.
        menu_id (int): The ID of the menu to retrieve.
    Returns:
        Menu: The menu object if found, otherwise returns None.
    """
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        return None
    return db_menu


def get_all_menus(session: Session) -> list[Menu]:
    """
    Retrieve all menus from the database.
    Args:
        session (Session): The database session.
    Returns:
        list[Menu]: A list of all menu objects.
    """
    statement = select(Menu)
    return session.exec(statement).all()


def get_menu_by_name(session: Session, name: str) -> Menu:
    """
    Retrieve a menu by its title from the database.
    Args:
        session (Session): The database session.
        name (str): The name of the menu to retrieve.
    Returns:
        Menu: The menu object if found, otherwise raises ValueError.
    """
    statement = select(Menu).where(Menu.name == name)
    db_menu = session.exec(statement).first()
    if not db_menu:
        return None
    return db_menu


def update_menu(
    session: Session, menu_id: int, menu_update: MenuUpdate
) -> Menu | None:
    """
    Update an existing menu in the database.
    Args:
        session (Session): The database session.
        menu_id (int): The ID of the menu to update.
        menu_update (MenuUpdate): The updated menu data.
    Returns:
        Menu: The updated menu object.
    """
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        return None

    menu_data = menu_update.model_dump(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)

    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


def delete_menu(session: Session, menu_id: int) -> None:
    """
    Delete a menu from the database.
    Args:
        session (Session): The database session.
        menu_id (int): The ID of the menu to delete.
    Raises:
        ValueError: If the menu with the given ID does not exist.
    """
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        return None

    session.delete(db_menu)
    session.commit()
