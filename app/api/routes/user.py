from typing import Any, List, Dict, Optional
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.auth.auth_handler import signJWT
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserPublicCreate,
    UserUpdate,
    UserPublic,
    UserLogin,
)
from app.schemas.order_schema import OrderPublic
from app.crud import user_crud, role_crud

from fastapi import Depends
from app.auth.auth_bearer import RoleChecker, TokenResponse
from app.models.role import RoleType

router = APIRouter(tags=["Users"])


def user_to_userpublic(user: User) -> UserPublic:
    roles_ids = [role.id for role in user.roles]
    return UserPublic(**user.model_dump(exclude={"roles"}), role_ids=roles_ids)


def userupdate_to_user(
    user_id: int, user_update: UserUpdate, session: SessionDep
) -> User:
    roles_in_user = []
    if user_update.role_ids:
        for role_id in user_update.role_ids:
            roles_in_user.append(
                role_crud.get_role_by_id(session=session, role_id=role_id)
            )
    return User(
        **user_update.model_dump(exclude={"role_ids"}),
        id=user_id,
        roles=roles_in_user,
    )


def usercreate_to_user(
    user_id: int, user_create: UserCreate, session: SessionDep
) -> User:
    roles_in_user = []
    for role_id in user_create.role_ids:
        roles_in_user.append(
            role_crud.get_role_by_id(session=session, role_id=role_id)
        )
    return User(
        **user_create.model_dump(exclude={"role_ids"}),
        id=user_id,
        roles=roles_in_user,
    )


@router.get(
    "/",
    response_model=List[UserPublic],
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_all_users(
    *,
    session: SessionDep,
) -> List[UserPublic]:
    users = user_crud.get_all_users(session=session)
    return [user_to_userpublic(user) for user in users]


@router.post("/signup", response_model=Dict[str, str])
def signup_user(
    *, session: SessionDep, user_schema_public_in: UserPublicCreate
):
    existing_user = user_crud.get_user_by_email(
        session, user_schema_public_in.email
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user already exists with this email."
        )

    # récupérer l'id du role "customer" pour l'affecter comme valeur par défaut
    #  à un user qui passe par /signup pour s'inscrit
    customer_role = role_crud.get_role_by_role_type(session, RoleType.customer)

    # pour la création d'un "employee" ou d'un admin,
    #  il faut passer par la route /post
    #  qui devrait être protégée APRES création d'un admin
    if customer_role is None:
        customer_role_id = 3
    else:
        if type(customer_role.id) is int:
            customer_role_id = customer_role.id
        else:
            customer_role_id = 3

    user_schema_in = UserCreate(
        username=user_schema_public_in.username,
        email=user_schema_public_in.email,
        first_name=user_schema_public_in.first_name,
        last_name=user_schema_public_in.last_name,
        adresse=user_schema_public_in.adresse,
        phone=user_schema_public_in.phone,
        password_hash=user_schema_public_in.password_hash,
        role_ids=[customer_role_id],
    )

    created_user = user_crud.create_user(session, user_schema_in)
    user_email = user_to_userpublic(created_user).email

    roles = [role.role_type.value for role in created_user.roles]
    mondict = signJWT(user_email, roles)
    return mondict


@router.post("/login", response_model=TokenResponse)
def login_user(*, session: SessionDep, user_schema_in: UserLogin):
    if user_crud.check_user(session, user_schema_in):
        user_info = user_crud.get_user_by_email(session, user_schema_in.email)
        roles = []
        if user_info:
            roles = [role.role_type.value for role in user_info.roles]
        else:
            roles.append("customer")
        return signJWT(user_schema_in.email, roles)

    return {"error": "Wrong login details!"}


@router.post("/", response_model=UserPublic)
def create_user(*, session: SessionDep, user_schema_in: UserCreate):
    existing_user = user_crud.get_user_by_email(session, user_schema_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user already exists with this email."
        )

    created_user = user_crud.create_user(session, user_schema_in)
    return user_to_userpublic(created_user)


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_user_by_id(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_userpublic(user_model)


@router.put(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(RoleChecker(allowed_roles=[RoleType.admin]))],
)
def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.email:
        user_with_same_email = user_crud.get_user_by_email(
            session=session, email=user_in.email
        )
        if user_with_same_email and (user_with_same_email.id != user_id):
            raise HTTPException(
                status_code=400,
                detail="An other user with the same email already exists.",
            )
    updated_user = user_crud.update_user(
        session=session,
        user_id=user_id,
        user_update=userupdate_to_user(user_id, user_in, session=session),
    )
    return user_to_userpublic(updated_user)


@router.delete(
    "/{user_id}",
    response_model=dict,
    dependencies=[Depends(RoleChecker(allowed_roles=[RoleType.admin]))],
)
def delete_user(*, session: SessionDep, user_id: int):
    user_model = user_crud.get_user_by_id(session=session, user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    user_crud.delete_user(session, user_id=user_id)
    return {"detail": "User deleted successfully"}


@router.get(
    "/{user_id}/orders",
    response_model=List[OrderPublic],
    dependencies=[
        Depends(RoleChecker(allowed_roles=[RoleType.admin, RoleType.employee]))
    ],
)
def get_all_orders_by_customer(*, session: SessionDep, user_id: int):
    return user_crud.get_all_orders_by_customer(session, user_id)
