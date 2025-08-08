from typing import List
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.models.user_role import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPublic
from app.crud import user_crud, role_crud

router = APIRouter(tags=["Users"])


def user_to_userpublic(user: User) -> UserPublic:
    roles_ids = [role.id for role in user.roles]
    return UserPublic(**user.model_dump(exclude={"roles"}), role_ids=roles_ids)


def userupdate_to_user(
    user_id: int, user_update: UserUpdate, session: SessionDep
) -> User:
    roles_in_user = []
    for role_id in user_update.role_ids:
        roles_in_user.append(role_crud.get_role_by_id(session=session, role_id=role_id))
    return User(
        **user_update.model_dump(exclude={"role_ids"}), id=user_id, roles=roles_in_user
    )


@router.get("/", response_model=List[UserPublic])
def get_all_users(*, session: SessionDep) -> List[UserPublic]:
    users = user_crud.get_all_users(session=session)
    return [user_to_userpublic(user) for user in users]


@router.post("/", response_model=UserPublic)
def create_user(*, session: SessionDep, user_schema_in: UserCreate):
    existing_user = user_crud.get_user_by_email(session, user_schema_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user already exists with this email."
        )

    created_user = user_crud.create_user(session, user_schema_in)
    return user_to_userpublic(created_user)


@router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_userpublic(user_model)


@router.put("/{user_id}", response_model=UserPublic)
def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_with_same_email = user_crud.get_user_by_email(
        session=session, email=user_in.email
    )
    if user_with_same_email and (user_with_same_email.id != user_id):
        raise HTTPException(
            status_code=400, detail="An other user with the same email already exists."
        )
    updated_user = user_crud.update_user(
        session=session,
        user_id=user_id,
        user_update=userupdate_to_user(user_id, user_in, session=session),
    )
    return user_to_userpublic(updated_user)


@router.delete("/{user_id}", response_model=dict)
def delete_user(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_crud.delete_user(session, user_id=user_id)
    return {"detail": "User deleted successfully"}
