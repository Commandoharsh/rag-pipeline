from fastapi import APIRouter, HTTPException

from backend.api.schemas import QueryRequest
from backend.rag.application import create_rag_application


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post("")
async def query_rag(request: QueryRequest):

    try:
        application = create_rag_application()

        result = application.query(
            question=request.question,
            conversation_context=request.conversation_context
        )

        citations = []

        for item in result.get("citations", []):
            citations.append({
                "source": item.metadata.get(
                    "source",
                    "unknown"
                ),
                "page": item.metadata.get(
                    "page",
                    "unknown"
                ),
                "chunk_id": item.chunk_id
            })

        return {
            "question": result["question"],
            "rewritten_query": result["rewritten_query"],
            "answer": result["answer"],
            "citations": citations
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        print(f"RAG query error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="RAG query failed."
        )