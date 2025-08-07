from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.user_schema import UserCreate, UserUpdate, UserPublic
from app.api.deps import SessionDep
from app.crud import user_crud

router = APIRouter(tags=["Users"])


@router.post("/", response_model=UserPublic)
def create_user(*, session: SessionDep, user_schema_in: UserCreate):
    existing_user_model = user_crud.get_user_by_email(
        session=session, email=user_schema_in.email
    )
    if existing_user_model:
        raise HTTPException(
            status_code=400,
            detail="A user already exists with this email.",
        )
    user_model = user_crud.create_user(session=session, menu=user_schema_in)
    return user_model


@router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.put("/{user_id}", response_model=dict)
def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_crud.update_crud(
        session=session, user_id=user_id, user_update=user_in
    )
    return updated_user


@router.delete("/{user_id}", response_model=dict)
def delete_user(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_crud.delete_user(session, user_id=user_id)
    return {"detail": "User deleted successfully"}
