# app/middleware/error_handler.py

from fastapi.responses import JSONResponse
from fastapi import Request

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )
