from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing import Dict, Any

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT


async def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> Dict[str, Any]:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    if credentials.scheme != "Bearer":
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
