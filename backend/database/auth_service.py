from datetime import datetime, timezone
from uuid import uuid4

from backend.api.security import (
    hash_password,
    verify_password,
)

from backend.api.auth import (
    create_access_token,
)

from backend.database.user_models import (
    UserRecord,
)


class AuthService:

    def __init__(
        self,
        repository,
    ):

        self.repository = repository

    def register(
        self,
        email: str,
        password: str,
    ):

        email = email.strip().lower()

        if not email:

            raise ValueError(
                "Email cannot be empty."
            )

        if len(password) < 8:

            raise ValueError(
                "Password must contain at least 8 characters."
            )

        existing = (
            self.repository.get_by_email(
                email
            )
        )

        if existing is not None:

            raise ValueError(
                "A user with this email already exists."
            )

        now = datetime.now(
            timezone.utc
        )

        user = UserRecord(
            id=str(uuid4()),
            email=email,
            password_hash=hash_password(
                password
            ),
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        self.repository.create(
            user
        )

        return user

    def authenticate(
        self,
        email: str,
        password: str,
    ):

        user = (
            self.repository.get_by_email(
                email.strip().lower()
            )
        )

        if user is None:

            return None

        if not user.is_active:

            return None

        if not verify_password(
            password,
            user.password_hash,
        ):

            return None

        token = create_access_token(
            user.id
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }