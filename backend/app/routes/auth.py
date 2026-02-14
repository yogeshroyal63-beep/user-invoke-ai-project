from fastapi import APIRouter
from pydantic import BaseModel
from app.services.auth_service import create_user, authenticate_user, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(req: AuthRequest):
    success = create_user(req.email, req.password)
    if not success:
        return {"error": "User already exists"}

    token = create_access_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
def login(req: AuthRequest):
    valid = authenticate_user(req.email, req.password)
    if not valid:
        return {"error": "Invalid credentials"}

    token = create_access_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
