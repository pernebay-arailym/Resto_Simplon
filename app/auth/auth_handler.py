from typing import Any, List, Optional
import jwt
from app.core.config import settings

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_TOKEN_EXPIRES = settings.JWT_TOKEN_EXPIRES


def token_response(token: str) -> dict[str, str]:
    return {"access_token": token}


def signJWT(user_id: str, user_roles: List[str]) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "roles": user_roles,
        "expires_in": int(JWT_TOKEN_EXPIRES),
        "token_type": "bearer",
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> Optional[dict[Any, Any]]:
    try:
        # La bibliothèque jwt gère automatiquement l'expiration du token
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return dict(decoded_token)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None
