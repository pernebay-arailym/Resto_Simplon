from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.schemas.role_schema import RoleCreate, RoleUpdate, RolePublic
from app.crud import role_crud

router = APIRouter(tags=["Roles"])


@router.get("/", response_model=list[RolePublic])
def get_all_roles(*, session: SessionDep) -> list[RolePublic]:
    return role_crud.get_all_roles(session=session)


@router.post("/", response_model=RolePublic)
def create_role(*, session: SessionDep, role_schema_in: RoleCreate):
    existing_role_model = role_crud.get_role_by_role_type(
        session=session, role_type=role_schema_in.role_type
    )
    if existing_role_model:
        raise HTTPException(
            status_code=400,
            detail="A role already exists with this role type.",
        )
    role_model = role_crud.create_role(session=session, role_schema=role_schema_in)
    return role_model


@router.get("/{role_id}", response_model=RolePublic)
def get_role_by_id(*, session: SessionDep, role_id: int):
    role_model = role_crud.get_role_by_id(session=session, role_id=role_id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_model


@router.put("/{role_id}", response_model=dict)
def update_role(*, session: SessionDep, role_id: int, role_in: RoleUpdate):
    role_model = role_crud.get_role_by_id(session=session, role_id=role_id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Role not found")
    role_with_same_role_type = role_crud.get_role_by_role_type(
        session=session, role_type=role_in.role_type
    )
    if (role_with_same_role_type is not None) and (
        role_with_same_role_type.id != role_id
    ):
        raise HTTPException(
            status_code=400,
            detail="An other role with the same role type already exists.",
        )
    updated_role = role_crud.update_crud(
        session=session, role_id=role_id, role_update=role_in
    )
    return updated_role


@router.delete("/{role_id}", response_model=dict)
def delete_role(*, session: SessionDep, role_id: int):
    role_model = role_crud.get_role_by_id(session=session, role_id=role_id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Role not found")

    role_crud.delete_role(session, role_id=role_id)
    return {"detail": "Role deleted successfully"}
