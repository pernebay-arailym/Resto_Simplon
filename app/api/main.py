from fastapi import APIRouter

from app.api.routes import user
from app.api.routes import role
from app.api.routes import menu
from app.api.routes import category
from app.api.routes import order
from app.api.routes import order_detail

router = APIRouter()
router.include_router(user.router, prefix="/users")
router.include_router(role.router, prefix="/roles")
router.include_router(menu.router, prefix="/menus")
router.include_router(category.router, prefix="/categories")
router.include_router(order.router, prefix="/orders")
router.include_router(order_detail.router, prefix="/orderdetails")

# Enfin, ce fichier relie toutes les routes de l’application :
# les utilisateurs, les rôles, les menus, les catégories, les commandes et les détails de commandes.
# Grâce à lui, FastAPI sait quelles routes utiliser et comment les regrouper.
# On peut donc accéder à toutes les fonctionnalités de l’application depuis un seul point central.
