from typing import List
from app.models.order import OrderBase
from app.schemas.order_schema import OrderPublic
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdate
from app.models import User, Role
from sqlmodel import Session, select
from app.auth.security import hash_password, verify_password


def create_user(session: Session, user_schema: UserCreate) -> User:
    new_user = User(
        username=user_schema.username,
        email=user_schema.email,
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        adresse=user_schema.adresse,
        phone=user_schema.phone,
        password_hash=hash_password(user_schema.password_hash),
    )

    roles = session.exec(
        select(Role).where(Role.id.in_(user_schema.role_ids))
    ).all()
    if len(roles) != len(user_schema.role_ids):
        raise ValueError("Un ou plusieurs role_ids sont invalides")

    new_user.roles = roles
    session.add(new_user)

    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_all_users(session: Session) -> list[User]:
    statement = select(User)
    return session.exec(statement).all()


def get_user_by_email(session: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    user_model = session.exec(statement).first()
    return user_model


def update_user(session: Session, user_id: int, user_update: User) -> User:
    user_model = session.get(User, user_id)
    if not user_model:
        raise ValueError("User not found")

    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_model, key, value)

    session.add(user_model)
    session.commit()
    session.refresh(user_model)
    return user_model


def delete_user(session: Session, user_id: int) -> None:
    user_model = session.get(User, user_id)
    if not user_model:
        raise ValueError("User not found")

    session.delete(user_model)
    session.commit()


def check_user(session: Session, user_schema: UserLogin) -> bool:
    user = get_user_by_email(session, user_schema.email)

    if user.email == user_schema.email and verify_password(
        user.password_hash, user_schema.password_hash
    ):
        return True
    return False


def get_all_orders_by_customer(
    session: Session, user_id: int
) -> List[OrderPublic]:
    statement = select(OrderBase).where(OrderBase.client_id == user_id)
    return session.exec(statement).all()
