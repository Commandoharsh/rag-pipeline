from datetime import datetime, timezone
from uuid import uuid4

from backend.database.conversation_models import ConversationRecord
from backend.database.message_models import MessageRecord


class ConversationRepository:

    def __init__(self, database):
        self.database = database

    # ---------------------------------------------------------
    # Conversations
    # ---------------------------------------------------------

    def create(
        self,
        user_id: str,
        title: str,
    ):
        now = datetime.now(timezone.utc)

        conversation = ConversationRecord(
            id=str(uuid4()),
            user_id=user_id,
            title=title.strip() or "New Conversation",
            created_at=now,
            updated_at=now,
        )

        with self.database._connect() as connection:
            connection.execute(
                """
                INSERT INTO conversations (
                    id,
                    user_id,
                    title,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    conversation.id,
                    conversation.user_id,
                    conversation.title,
                    conversation.created_at.isoformat(),
                    conversation.updated_at.isoformat(),
                ),
            )

            connection.commit()

        return conversation

    def get(self, conversation_id: str):
        with self.database._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM conversations
                WHERE id = ?
                """,
                (conversation_id,),
            ).fetchone()

        if row is None:
            return None

        return self._conversation_from_row(row)

    def get_for_user(
        self,
        conversation_id: str,
        user_id: str,
    ):
        with self.database._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM conversations
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    conversation_id,
                    user_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._conversation_from_row(row)

    def list_for_user(self, user_id: str):
        with self.database._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM conversations
                WHERE user_id = ?
                ORDER BY updated_at DESC
                """,
                (user_id,),
            ).fetchall()

        return [
            self._conversation_from_row(row)
            for row in rows
        ]

    def delete_for_user(
        self,
        conversation_id: str,
        user_id: str,
    ):
        with self.database._connect() as connection:

            conversation = connection.execute(
                """
                SELECT id
                FROM conversations
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    conversation_id,
                    user_id,
                ),
            ).fetchone()

            if conversation is None:
                return False

            # Delete messages first.
            connection.execute(
                """
                DELETE FROM messages
                WHERE conversation_id = ?
                """,
                (conversation_id,),
            )

            connection.execute(
                """
                DELETE FROM conversations
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    conversation_id,
                    user_id,
                ),
            )

            connection.commit()

        return True

    def touch(self, conversation_id: str):
        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self.database._connect() as connection:
            connection.execute(
                """
                UPDATE conversations
                SET updated_at = ?
                WHERE id = ?
                """,
                (
                    updated_at,
                    conversation_id,
                ),
            )

            connection.commit()

    # ---------------------------------------------------------
    # Messages
    # ---------------------------------------------------------

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):
        allowed_roles = {
            "user",
            "assistant",
            "system",
        }

        if role not in allowed_roles:
            raise ValueError(
                f"Invalid message role: {role}"
            )

        if not content.strip():
            raise ValueError(
                "Message content cannot be empty."
            )

        message = MessageRecord(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )

        with self.database._connect() as connection:
            connection.execute(
                """
                INSERT INTO messages (
                    id,
                    conversation_id,
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    message.id,
                    message.conversation_id,
                    message.role,
                    message.content,
                    message.created_at.isoformat(),
                ),
            )

            connection.commit()

        self.touch(conversation_id)

        return message

    def get_messages(
        self,
        conversation_id: str,
    ):
        with self.database._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC
                """,
                (conversation_id,),
            ).fetchall()

        return [
            self._message_from_row(row)
            for row in rows
        ]

    def get_recent_messages(
        self,
        conversation_id: str,
        limit: int = 10,
    ):
        if limit <= 0:
            return []

        with self.database._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (
                    conversation_id,
                    limit,
                ),
            ).fetchall()

        messages = [
            self._message_from_row(row)
            for row in rows
        ]

        messages.reverse()

        return messages

    # ---------------------------------------------------------
    # Converters
    # ---------------------------------------------------------

    @staticmethod
    def _conversation_from_row(row):
        return ConversationRecord(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
        )

    @staticmethod
    def _message_from_row(row):
        return MessageRecord(
            id=row["id"],
            conversation_id=row["conversation_id"],
            role=row["role"],
            content=row["content"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
        )