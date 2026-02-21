from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router
from app.routes.auth import router as auth_router
from app.routes.url_scan import router as url_router
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.error_handler import global_exception_handler
from app.routes.unified_scan import router as unified_scan_router

app = FastAPI(title="TrustCheck AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(unified_scan_router)

app.add_middleware(RateLimitMiddleware)
app.include_router(url_router)
app.include_router(auth_router)
app.include_router(analyze_router)

@app.get("/")
def root():
    return {"status": "running"}
