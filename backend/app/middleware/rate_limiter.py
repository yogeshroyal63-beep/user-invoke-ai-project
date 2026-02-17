# app/middleware/rate_limiter.py

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

RATE_LIMIT = 20  # requests
WINDOW = 60      # seconds

clients = {}

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        if ip not in clients:
            clients[ip] = []

        clients[ip] = [t for t in clients[ip] if now - t < WINDOW]

        if len(clients[ip]) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests"}
            )

        clients[ip].append(now)
        response = await call_next(request)
        return response
