import sys, os
# Ajoute le répertoire parent au chemin pour l'importation des modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from app.api.main import router
from app.core.config import settings

# on utilise alembic pour la création de la BDD...
# from app.core.database import create_db_and_tables, get_session, engine


# Définition de la fonction lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Fonction de cycle de vie de l'application.
    Exécute des tâches au démarrage et à l'arrêt.
    """
    print("Application en cours de démarrage...")
    # on passe par alembic pour la création de la BDD
    # # Crée les tables de la base de données au démarrage
    # create_db_and_tables()
    # Le 'yield' indique que l'application est maintenant démarrée et prête à servir
    yield
    print("Application en cours d'arrêt...")
    # Ici, vous pouvez ajouter du code pour fermer des connexions, etc.
    # Dans le cas de SQLModel, l'engine est géré automatiquement,
    # mais vous pourriez fermer d'autres types de connexions (Redis, etc.).
    # engine.dispose() # Par exemple, si vous vouliez forcer la fermeture


# Crée l'application FastAPI en passant la fonction lifespan
app = FastAPI(lifespan=lifespan)

# Gestion des CORS qu'il faudra très certainement activer
# # Set all CORS enabled origins
# if settings.all_cors_origins:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.all_cors_origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# Include the API router
app.include_router(router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # crée deux roles par défaut dans la BDD
    from app.core.database import create_db_and_tables
    create_db_and_tables()

    from app.crud.role_crud import create_role, get_all_roles
    from app.models.user_role import RoleType
    from app.schemas.role_schema import RoleCreate
    from app.core.database import get_session
    session = next(get_session())
    print("Création des rôles par défaut...")

    # Création des rôles par défaut seulement si aucun rôle n'existe
    existing_roles = get_all_roles(session)
    if not existing_roles:
        role_admin = RoleCreate(
            role_type=RoleType.admin,
            name="Administrator",
            description="Administrator role with full access"
        )
        create_role(session, role_admin)

        role_customer = RoleCreate(
            role_type=RoleType.customer,
            name="customer",
            description="Regular customer role with limited access"
        )
        create_role(session, role_customer)
        print("Rôles par défaut créés.")
    else:
        print("Les rôles existent déjà en base, aucune création nécessaire.")

    # lance l'application FastAPI
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8050, log_level="info", reload=True)