from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.api.dependencies import get_current_user
from backend.database.database import Database
from backend.database.conversation_repository import (
    ConversationRepository,
)
from backend.rag.application import create_rag_application


router = APIRouter(
    prefix="/conversations",
    tags=["Conversation RAG"],
)


database = Database()

conversation_repository = ConversationRepository(
    database
)


class ConversationQueryRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=10000,
    )


def build_conversation_context(
    messages,
):
    if not messages:
        return None

    lines = []

    for message in messages:
        role = message.role.upper()

        lines.append(
            f"{role}: {message.content}"
        )

    return "\n".join(lines)


@router.post("/{conversation_id}/query")
def query_conversation(
    conversation_id: str,
    request: ConversationQueryRequest,
    current_user=Depends(get_current_user),
):
    # -----------------------------------------------------
    # 1. Validate conversation ownership
    # -----------------------------------------------------

    conversation = conversation_repository.get_for_user(
        conversation_id,
        current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # -----------------------------------------------------
    # 2. Retrieve recent conversation history
    # -----------------------------------------------------

    previous_messages = (
        conversation_repository.get_recent_messages(
            conversation_id=conversation_id,
            limit=10,
        )
    )

    conversation_context = (
        build_conversation_context(
            previous_messages
        )
    )

    # -----------------------------------------------------
    # 3. Save user's question
    # -----------------------------------------------------

    user_message = (
        conversation_repository.add_message(
            conversation_id=conversation_id,
            role="user",
            content=question,
        )
    )

    # -----------------------------------------------------
    # 4. Run ResearchRAG
    # -----------------------------------------------------

    try:
        application = create_rag_application()

        result = application.query(
            question=question,
            conversation_context=conversation_context,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        print(
            f"Conversation RAG error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="RAG query failed.",
        )

    # -----------------------------------------------------
    # 5. Extract answer
    # -----------------------------------------------------

    answer = result.get(
        "answer",
        "",
    )

    if not answer:
        raise HTTPException(
            status_code=500,
            detail="RAG returned an empty answer.",
        )

    # -----------------------------------------------------
    # 6. Save assistant answer
    # -----------------------------------------------------

    assistant_message = (
        conversation_repository.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )
    )

    # -----------------------------------------------------
    # 7. Prepare citations
    # -----------------------------------------------------

    citations = []

    for item in result.get(
        "results",
        [],
    ):
        citations.append(
            {
                "chunk_id": item.chunk_id,
                "source": item.metadata.get(
                    "source",
                    "unknown",
                ),
                "page": item.metadata.get(
                    "page",
                    "unknown",
                ),
            }
        )

    # -----------------------------------------------------
    # 8. Return complete response
    # -----------------------------------------------------

    return {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer,
        "rewritten_query": result.get(
            "rewritten_query"
        ),
        "queries": result.get(
            "queries",
            [],
        ),
        "citations": citations,
        "messages": {
            "user": {
                "id": user_message.id,
                "role": user_message.role,
            },
            "assistant": {
                "id": assistant_message.id,
                "role": assistant_message.role,
            },
        },
    }