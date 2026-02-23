# app/middleware/error_handler.py

from fastapi.responses import JSONResponse
from fastapi import Request


async def global_exception_handler(request: Request, exc: Exception):
    print("UNHANDLED ERROR:", str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "type": "chat",
            "reply": "Internal server error."
        }
    )