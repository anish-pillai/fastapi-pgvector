from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.models import Message
from app.schemas import MessageCreate, MessageResponse

router = APIRouter()


@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(chat_id=message.chat_id, role=message.role, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: UUID, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message