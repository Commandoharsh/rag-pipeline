import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("researchrag.errors")


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Centralized exception handler.

    Logs detailed server-side information while returning
    a safe response to the client.
    """

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.error(
        "Unhandled exception | "
        "request_id=%s | "
        "method=%s | "
        "path=%s | "
        "error_type=%s | "
        "error=%s",
        request_id,
        request.method,
        request.url.path,
        type(exc).__name__,
        str(exc),
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error.",
            "request_id": request_id,
        },
    )