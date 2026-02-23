from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi.responses import JSONResponse
import os

from app.routes.unified_scan import router as unified_scan_router
from app.routes.url_scan import router as url_router
from app.routes.file_scan import router as file_router
from app.routes.auth import router as auth_router
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.error_handler import global_exception_handler


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

API_KEY = os.getenv("TRUSTCHECK_API_KEY", "trustcheck-secret")
API_KEY_NAME = "x-api-key"

app = FastAPI(
    title="TrustCheck AI",
    version="2.0",
    docs_url="/docs",
    redoc_url=None
)


# =========================
# SECURITY HEADERS
# =========================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self';"
        )

        return response


# =========================
# API KEY MIDDLEWARE
# =========================

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path.startswith("/api/auth"):
            return await call_next(request)

        key = request.headers.get("x-api-key")

        if key != API_KEY:
            return JSONResponse(
                status_code=403,
                content={"error": "Forbidden - Invalid API Key"}
            )

        return await call_next(request)


# =========================
# MIDDLEWARE
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", API_KEY_NAME],
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(APIKeyMiddleware)
app.add_middleware(RateLimitMiddleware)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(unified_scan_router)
app.include_router(url_router)
app.include_router(file_router)
app.include_router(auth_router)


# =========================
# OPENAPI SECURITY
# =========================

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="TrustCheck AI",
        version="2.0",
        description="Enterprise Cybersecurity Intelligence API",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key",
        }
    }

    openapi_schema["security"] = [{"ApiKeyAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "TrustCheck AI",
        "version": "2.0"
    }