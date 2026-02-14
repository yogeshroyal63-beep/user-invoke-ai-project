from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router
from app.routes.auth import router as auth_router
from app.routes.image_scan import router as image_router
from app.routes.url_scan import router as url_router

app = FastAPI(title="TrustCheck AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router)
app.include_router(image_router)
app.include_router(auth_router)
app.include_router(analyze_router)

@app.get("/")
def root():
    return {"status": "running"}
