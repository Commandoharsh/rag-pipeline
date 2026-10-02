from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from backend.api.schemas import QueryRequest

from backend.rag.application import (
    create_rag_application
)

from backend.rag.generation.prompt_templates import (
    SYSTEM_PROMPT,
    build_prompt
)


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post("/stream")
async def stream_query(
    request: QueryRequest
):

    application = (
        create_rag_application()
    )

    prepared = (
        application.rag_service.prepare(
            question=request.question,
            conversation_context=(
                request.conversation_context
            )
        )
    )

    prompt = build_prompt(
        question=prepared["question"],
        context=prepared["context"]
    )

    def generate():

        for token in application.llm.stream(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT
        ):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )