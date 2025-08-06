from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.models.category import Category
from sqlmodel import Session, select


def create_category(session: Session, category: CategoryCreate) -> Category:
    """
    Create a new category in the database.
    Args:
        session (Session): The database session.
        category (CategoryCreate): The category data to create.
    Returns:
        Category: The created category.
    """
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def get_category_by_id(session: Session, category_id: int) -> Category:
    """
    Retrieve a category by ID from the database.
    Args:
        session (Session): The database session.
        category_id (int): The ID of the category to retrieve.
    Returns:
        Category: The category object if found, otherwise raises ValueError.
    """
    db_category = session.get(Category, category_id)
    if not db_category:
        raise ValueError("Category not found")
    return db_category


def get_all_categories(session: Session) -> list[Category]:
    """
    Retrieve all categories from the database.
    Args:
        session (Session): The database session.
    Returns:
        list[Category]: A list of all category objects.
    """
    statement = select(Category)
    return session.exec(statement).all()


def get_category_by_name(session: Session, name: str) -> Category:
    """
    Retrieve a category by its title from the database.
    Args:
        session (Session): The database session.
        name (str): The name of the category to retrieve.
    Returns:
        Category: The category object if found, otherwise raises ValueError.
    """
    statement = select(Category).where(Category.name == name)
    db_category = session.exec(statement).first()
    return db_category


def update_category(
    session: Session, category_id: int, category_update: CategoryUpdate
) -> Category:
    """
    Update an existing category in the database.
    Args:
        session (Session): The database session.
        category_id (int): The ID of the category to update.
        category_update (CategoryUpdate): The updated category data.
    Returns:
        Category: The updated category object.
    """
    db_category = session.get(Category, category_id)
    if not db_category:
        raise ValueError("Category not found")

    category_data = category_update.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def delete_category(session: Session, category_id: int) -> None:
    """
    Delete a category from the database.
    Args:
        session (Session): The database session.
        category_id (int): The ID of the category to delete.
    Raises:
        ValueError: If the category with the given ID does not exist.
    """
    db_category = session.get(Category, category_id)
    if not db_category:
        raise ValueError("Category not found")

    session.delete(db_category)
    session.commit()
