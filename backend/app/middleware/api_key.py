# app/middleware/api_key.py

from fastapi import Request
from fastapi.responses import JSONResponse

API_KEY = "trustcheck-secret"

async def verify_api_key(request: Request, call_next):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    return await call_next(request)
