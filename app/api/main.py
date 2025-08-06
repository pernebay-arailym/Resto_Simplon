from fastapi import APIRouter

from app.api.routes import user
from app.api.routes import menu

router = APIRouter()
router.include_router(
    user.router, prefix="/users"
)  # param supplémentaire ?? , tags=["trainees"]
router.include_router(menu.router, prefix="/menus")
