# app/middleware/error_handler.py

from fastapi.responses import JSONResponse
from fastapi import Request
import traceback
import logging

logger = logging.getLogger("trustcheck")


async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler.
    Logs full traceback internally.
    Returns sanitized error to client.
    """

    # Log full traceback for internal debugging
    logger.error("Unhandled Exception", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "type": "error",
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing your request."
        }
    )