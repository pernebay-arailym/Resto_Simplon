from app.schemas.role_schema import RoleCreate, RoleUpdate
from app.models.user_role import Role, RoleType
from sqlmodel import Session, select


def create_role(session: Session, role_schema: RoleCreate) -> Role:
    role_model = Role.model_validate(role_schema)
    session.add(role_model)
    session.commit()
    session.refresh(role_model)
    return role_model


def get_role_by_id(session: Session, role_id: int) -> Role | None:
    return session.get(Role, role_id)


def get_role_by_role_type(session: Session, role_type: RoleType) -> Role:
    statement = select(Role).where(Role.role_type == role_type)
    role_model = session.exec(statement).first()
    return role_model


def get_all_roles(session: Session) -> list[Role]:
    statement = select(Role)
    return session.exec(statement).all()


def update_role(session: Session, role_id: int, role_update: RoleUpdate) -> Role:
    role_model = session.get(Role, role_id)
    if not role_model:
        raise ValueError("Role not found")

    role_data = role_update.model_dump(exclude_unset=True)
    for key, value in role_data.items():
        setattr(role_model, key, value)

    session.add(role_model)
    session.commit()
    session.refresh(role_model)
    return role_model


def delete_role(session: Session, role_id: int) -> None:
    role_model = session.get(Role, role_id)
    if not role_model:
        raise ValueError("Role not found")

    session.delete(role_model)
    session.commit()
