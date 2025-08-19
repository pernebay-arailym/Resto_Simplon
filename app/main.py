from contextlib import asynccontextmanager
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
