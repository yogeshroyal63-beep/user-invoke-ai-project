# app/core/limiter.py

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.core.config import settings


# =====================================================
# GLOBAL LIMITER INSTANCE
# =====================================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT}/{settings.RATE_WINDOW}seconds"]
)


# =====================================================
# RATE LIMIT HANDLER
# =====================================================

def rate_limit_exceeded_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "retry_after_seconds": settings.RATE_WINDOW
        }
    )