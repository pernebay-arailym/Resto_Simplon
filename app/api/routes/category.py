from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.category_schema import CategoryCreate, CategoryPublic, CategoryUpdate
from app.crud import category_crud
from typing import List

router = APIRouter(tags=["Categories"])


@router.get("/", response_model=List[CategoryPublic])
def get_all_categories(*, session: SessionDep):
    """
    Get all categories.

    Args:
        session (SessionDep): The database session dependency.
        category_id (int): The ID of the category to retrieve.

    Raises:
        HTTPException: If the category is not found.

    Returns:
        CategoryPublic: The retrieved category data.
    """
    return category_crud.get_all_categories(session=session)


@router.post("/", response_model=CategoryPublic)
def create_category(*, session: SessionDep, category_in: CategoryCreate):
    """
    Create a new category.

    Args:
        session (SessionDep): The database session dependency.
        category_in (CategoryCreate): The category creation data.

    Raises:
        HTTPException: If the category with this name already exists.
        HTTPException: If the category creation fails.

    Returns:
        CategoryPublic: The created category data.
    """

    category = category_crud.get_category_by_name(
        session=session, name=category_in.name
    )
    if category:
        raise HTTPException(
            status_code=400,
            detail="The category with this name already exists in the system.",
        )

    category = category_crud.create_category(session=session, category=category_in)

    return category


@router.get("/{category_id}", response_model=CategoryPublic)
def get_category_by_id(*, session: SessionDep, category_id: int):
    """
    Get a category by ID.

    Args:
        session (SessionDep): The database session dependency.
        category_id (int): The ID of the category to retrieve.

    Raises:
        HTTPException: If the category is not found.

    Returns:
        CategoryPublic: The retrieved category data.
    """
    category = category_crud.get_category_by_id(
        session=session, category_id=category_id
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.put("/{category_id}", response_model=CategoryPublic)
def update_category(
    *, session: SessionDep, category_id: int, category_in: CategoryUpdate
):
    """
    Update a category by ID.

    Args:
        session (SessionDep): The database session dependency.
        category_id (int): The ID of the category to update.
        category_in (CategoryCreate): The category update data.

    Raises:
        HTTPException: If the category is not found.
        HTTPException: If the category update fails.

    Returns:
        CategoryPublic: The updated category data.
    """

    category = category_crud.get_category_by_id(
        session=session, category_id=category_id
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    updated_category = category_crud.update_category(
        session=session, category_id=category_id, category_update=category_in
    )

    return updated_category


@router.delete("/{category_id}", response_model=dict)
def delete_category(*, session: SessionDep, category_id: int):
    """
    Delete a category by ID.

    Args:
        session (SessionDep): The database session dependency.
        category_id (int): The ID of the category to delete.

    Raises:
        HTTPException: If the category is not found.

    Returns:
        dict: A success message.
    """

    category = category_crud.get_category_by_id(
        session=session, category_id=category_id
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_crud.delete_category(session=session, category_id=category_id)

    return {"detail": "Category deleted successfully"}
