# app/routes/file_scan.py

from fastapi import APIRouter, UploadFile, File
from app.services.file_scanner import scan_file

router = APIRouter(prefix="/api")

@router.post("/scan-file")
async def scan_uploaded_file(file: UploadFile = File(...)):
    content = await file.read()
    return scan_file(file.filename, content)
