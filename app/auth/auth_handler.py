import time
from typing import Dict, Optional
import os
import jwt
from app.core.config import settings

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return {"access_token": token}


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "exp": time.time() + 900}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token_response(token)


# def signJWT(user_id: str, user_role: str) -> Dict[str, str]:
#     payload = {"user_id": user_id, "user_role": user_role, "exp": time.time() + 900}
#     token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
#     return token_response(token)


def decodeJWT(token: str) -> Optional[dict]:
    try:
        # La bibliothèque jwt gère automatiquement l'expiration du token
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Cette erreur est affichée si le token a expiré (plus de 15 minutes)
        print("Erreur de décodage : le token est expiré.")
        return None
    except jwt.InvalidTokenError:
        # Cette erreur est affichée si la clé secrète ne correspond pas ou si le token est mal formé
        print(
            "Erreur de décodage : le token est invalide (signature incorrecte, etc.)."
        )
        return None
    except Exception as e:
        # Pour toute autre erreur inattendue
        print(f"Erreur inattendue lors du décodage du JWT : {e}")
        return None
