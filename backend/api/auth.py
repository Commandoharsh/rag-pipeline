from datetime import datetime, timedelta, timezone

import jwt

from backend.config import settings


def create_access_token(
    user_id: str,
) -> str:
    """
    Create a JWT access token for a user.
    """

    now = datetime.now(timezone.utc)

    expires = now + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
):
    """
    Decode and validate a JWT access token.

    Returns:
        dict: decoded payload if valid
        None: if token is invalid or expired
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

        return payload

    except jwt.InvalidTokenError:
        return None