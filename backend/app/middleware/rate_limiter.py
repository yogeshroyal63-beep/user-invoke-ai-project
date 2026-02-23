# app/middleware/rate_limiter.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

RATE_LIMIT = 20
WINDOW_SECONDS = 60

request_store = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in request_store:
            request_store[client_ip] = []

        request_store[client_ip] = [
            t for t in request_store[client_ip]
            if current_time - t < WINDOW_SECONDS
        ]

        if len(request_store[client_ip]) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests. Please slow down."}
            )

        request_store[client_ip].append(current_time)

        return await call_next(request)