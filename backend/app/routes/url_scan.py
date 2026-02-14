from fastapi import APIRouter
from pydantic import BaseModel
from app.services.url_trust_engine import scan_url

router = APIRouter(prefix="/api")

class UrlReq(BaseModel):
    url: str

@router.post("/scan-url")
def scan(req: UrlReq):
    return scan_url(req.url)
