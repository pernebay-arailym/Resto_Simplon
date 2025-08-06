from fastapi import APIRouter, HTTPException
#from app.schemas.user_schema import UserCreate, UserPublic
# à voir si on a besoin de faireil que ds le projet de référence : from app.api.deps import SessionDep
#from app.crud import user_crud # pour gérer les opérations de base CRUD pour les users

router = APIRouter(prefix="/users") # param optionnel à ajouter ? , tags=["trainees"]

#@router.post("/", response_model=UserPublic)
#def create_user(*, session: SessionDep, trainee_in: TraineeCreate):