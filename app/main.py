from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
#from app.models.hero import Hero
from app.core.database import create_db_and_tables, get_session, engine


# Définition de la fonction lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Fonction de cycle de vie de l'application.
    Exécute des tâches au démarrage et à l'arrêt.
    """
    print("Application en cours de démarrage...")
    # Crée les tables de la base de données au démarrage
    create_db_and_tables() 
    # Le 'yield' indique que l'application est maintenant démarrée et prête à servir
    yield
    print("Application en cours d'arrêt...")
    # Ici, vous pouvez ajouter du code pour fermer des connexions, etc.
    # Dans le cas de SQLModel, l'engine est géré automatiquement,
    # mais vous pourriez fermer d'autres types de connexions (Redis, etc.).
    # engine.dispose() # Par exemple, si vous vouliez forcer la fermeture

# Crée l'application FastAPI en passant la fonction lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
