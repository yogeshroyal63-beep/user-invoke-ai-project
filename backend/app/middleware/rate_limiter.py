# app/middleware/rate_limiter.py

import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import threading


RATE_LIMIT = 20   # requests
WINDOW = 60       # seconds

# In-memory store
clients = defaultdict(list)
lock = threading.Lock()


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        ip = request.client.host
        now = time.time()

        with lock:
            # Remove expired timestamps
            clients[ip] = [t for t in clients[ip] if now - t < WINDOW]

            if len(clients[ip]) >= RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Too many requests",
                        "retry_after_seconds": WINDOW
                    }
                )

            clients[ip].append(now)

        response = await call_next(request)
        return response