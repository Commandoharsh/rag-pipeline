from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile
)

from backend.rag.application import (
    create_rag_application
)


router = APIRouter(
    prefix="/index",
    tags=["Indexing"]
)


DATA_DIR = Path("data/raw")

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/pdf")
async def index_pdf(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    safe_filename = (
        Path(file.filename).name
    )

    if not safe_filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    destination = (
        DATA_DIR / safe_filename
    )

    try:

        with destination.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        application = (
            create_rag_application()
        )

        result = application.index_pdf(
            str(destination)
        )

        return {
            "status": "success",
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

    finally:

        await file.close()
    MAX_UPLOAD_SIZE = (
    25 * 1024 * 1024
)