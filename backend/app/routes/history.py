from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.chat_model import ChatMessage

router = APIRouter(prefix="/api/history")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{email}")
def get_history(email: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage)\
        .filter(ChatMessage.user_email == email)\
        .order_by(ChatMessage.created_at).all()

    return [
        {
            "role": m.role,
            "text": m.content
        } for m in messages
    ]
