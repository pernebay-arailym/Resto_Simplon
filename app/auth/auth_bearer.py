from typing import List
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from app.auth.auth_handler import decodeJWT


security = HTTPBearer()


# Modèle pour la réponse JWT
class TokenResponse(BaseModel):
    access_token: str


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            decoded_payload = decodeJWT(credentials.credentials)
            if not decoded_payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token.",
                )
            return decoded_payload
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )


# Dépendance pour vérifier les rôles
# On passe la liste des rôles autorisés à l'initialisation
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(JWTBearer())):

        user_roles = payload.get("roles")
        user_allowed = False
        for user_role in user_roles:
            if user_role in self.allowed_roles:
                user_allowed = True
                break

        if not user_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        # Si le rôle est valide, on ne fait rien et on continue vers la route
        return True
