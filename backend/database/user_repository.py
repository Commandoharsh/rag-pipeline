from datetime import datetime, timezone

from backend.database.database import Database
from backend.database.user_models import UserRecord


class UserRepository:

    def __init__(
        self,
        database: Database,
    ):

        self.database = database

    def create(
        self,
        user: UserRecord,
    ):

        with self.database._connect() as connection:

            connection.execute(
                """
                INSERT INTO users (
                    id,
                    email,
                    password_hash,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user.id,
                    user.email,
                    user.password_hash,
                    int(user.is_active),
                    user.created_at.isoformat(),
                    user.updated_at.isoformat(),
                ),
            )

            connection.commit()

        return user

    def get_by_id(
        self,
        user_id: str,
    ):

        with self.database._connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

        if row is None:
            return None

        return self._to_user(row)

    def get_by_email(
        self,
        email: str,
    ):

        with self.database._connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM users
                WHERE email = ?
                """,
                (email,),
            ).fetchone()

        if row is None:
            return None

        return self._to_user(row)

    @staticmethod
    def _to_user(row):

        return UserRecord(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            is_active=bool(
                row["is_active"]
            ),
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
        )