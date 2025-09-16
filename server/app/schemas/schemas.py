from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime


# -------------------
# User Schemas
# -------------------
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID4
    username: str
    email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Chat Schemas
# -------------------
class ChatCreate(BaseModel):
    title: Optional[str] = None
    user_id: UUID4


class ChatResponse(BaseModel):
    id: UUID4
    title: Optional[str] = None
    user_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Message Schemas
# -------------------
class MessageCreate(BaseModel):
    chat_id: UUID4
    role: str
    content: str


class MessageResponse(BaseModel):
    id: UUID4
    chat_id: UUID4
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Document Schemas
# -------------------
class DocumentCreate(BaseModel):
    filename: str
    doc_metadata: Optional[dict] = None
    content: str
    embedding: List[float]


class DocumentResponse(BaseModel):
    id: UUID4
    filename: str
    doc_metadata: Optional[dict]
    content: str

    class Config:
        from_attributes = True