from fastapi import APIRouter

from app.api.routes import user
from app.api.routes import menu
from app.api.routes import category


router = APIRouter()
router.include_router(user.router, prefix="/users")
router.include_router(menu.router, prefix="/menus")
router.include_router(category.router, prefix="/categories")
