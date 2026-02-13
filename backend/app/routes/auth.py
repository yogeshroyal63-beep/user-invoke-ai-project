from fastapi import APIRouter
from pydantic import BaseModel
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(req: RegisterRequest):
    user = create_user(req.email, req.password)
    token = create_access_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
def login(req: LoginRequest):
    user = authenticate_user(req.email, req.password)
    if not user:
        return {"error": "Invalid credentials"}

    token = create_access_token(req.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
