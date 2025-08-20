from typing import Any, Dict, List, Optional
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.auth.auth_handler import decodeJWT


security = HTTPBearer()


# Modèle pour la réponse JWT
class TokenResponse(BaseModel):
    access_token: str


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JWTBearer, self
        ).__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )

        return credentials


# Dépendance pour vérifier les rôles
# On passe la liste des rôles autorisés à l'initialisation
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(JWTBearer())):

        user_roles = payload.get("roles")
        user_allowed = False
        if user_roles:
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
