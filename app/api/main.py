from fastapi import APIRouter

from app.api.routes import user
from app.api.routes import menu
from app.api.routes import category
from app.api.routes import order
from app.api.routes import order_detail

router = APIRouter()
router.include_router(user.router, prefix="/users")
router.include_router(menu.router, prefix="/menus")
router.include_router(category.router, prefix="/categories")
router.include_router(order.router, prefix="/orders")
router.include_router(order_detail.router, prefix="/orderdetails")
