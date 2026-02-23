from fastapi import APIRouter
from pydantic import BaseModel
from app.services.url_trust_engine import scan_url

router = APIRouter(prefix="/api", tags=["URL Scan"])


class URLRequest(BaseModel):
    url: str


@router.post("/scan-url")
def scan_url_route(req: URLRequest):
    result = scan_url(req.url)
    return result