from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.api.dependencies import get_current_user
from backend.database.database import Database
from backend.database.conversation_repository import (
    ConversationRepository,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


database = Database()

repository = ConversationRepository(
    database
)


# ---------------------------------------------------------
# Schemas
# ---------------------------------------------------------

class CreateConversationRequest(BaseModel):
    title: str = Field(
        default="New Conversation",
        max_length=200,
    )


class AddMessageRequest(BaseModel):
    role: str
    content: str = Field(
        min_length=1,
        max_length=100000,
    )


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def serialize_conversation(conversation):
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
    }


def serialize_message(message):
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at,
    }


# ---------------------------------------------------------
# Create conversation
# ---------------------------------------------------------

@router.post("")
def create_conversation(
    request: CreateConversationRequest,
    current_user=Depends(get_current_user),
):
    conversation = repository.create(
        user_id=current_user.id,
        title=request.title,
    )

    return {
        "conversation": serialize_conversation(
            conversation
        )
    }


# ---------------------------------------------------------
# List user's conversations
# ---------------------------------------------------------

@router.get("")
def list_conversations(
    current_user=Depends(get_current_user),
):
    conversations = repository.list_for_user(
        current_user.id
    )

    return {
        "conversations": [
            serialize_conversation(
                conversation
            )
            for conversation in conversations
        ]
    }


# ---------------------------------------------------------
# Get one conversation
# ---------------------------------------------------------

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    conversation = repository.get_for_user(
        conversation_id,
        current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    messages = repository.get_messages(
        conversation_id
    )

    return {
        "conversation": serialize_conversation(
            conversation
        ),
        "messages": [
            serialize_message(message)
            for message in messages
        ],
    }


# ---------------------------------------------------------
# Delete conversation
# ---------------------------------------------------------

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    deleted = repository.delete_for_user(
        conversation_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "status": "deleted",
        "conversation_id": conversation_id,
    }


# ---------------------------------------------------------
# Add message manually
# ---------------------------------------------------------

@router.post("/{conversation_id}/messages")
def add_message(
    conversation_id: str,
    request: AddMessageRequest,
    current_user=Depends(get_current_user),
):
    conversation = repository.get_for_user(
        conversation_id,
        current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    if request.role not in {
        "user",
        "assistant",
        "system",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid role. "
                "Use user, assistant, or system."
            ),
        )

    message = repository.add_message(
        conversation_id=conversation_id,
        role=request.role,
        content=request.content,
    )

    return {
        "message": serialize_message(message)
    }


# ---------------------------------------------------------
# Get messages
# ---------------------------------------------------------

@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    conversation = repository.get_for_user(
        conversation_id,
        current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    messages = repository.get_messages(
        conversation_id
    )

    return {
        "messages": [
            serialize_message(message)
            for message in messages
        ]
    }