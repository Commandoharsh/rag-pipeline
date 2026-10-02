from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.api.auth import decode_access_token
from backend.database.database import Database
from backend.database.user_repository import UserRepository


security = HTTPBearer()


database = Database()

user_repository = UserRepository(
    database
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token.",
        )

    user = user_repository.get_by_id(
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive.",
        )

    return user