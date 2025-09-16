from sqlalchemy import Column, Text, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

# -------------------
# Users Table
# -------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=generate_uuid)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", back_populates="user")
    documents = relationship("Document", back_populates="user")


# -------------------
# Chats Table
# -------------------
class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID, primary_key=True, index=True, default=generate_uuid)
    title = Column(Text, nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")


# -------------------
# Messages Table
# -------------------
class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True, index=True, default=generate_uuid)
    chat_id = Column(UUID, ForeignKey("chats.id"), nullable=False)
    role = Column(Text, nullable=False)  # e.g. "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages")


# -------------------
# Documents Table
# -------------------
class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID, primary_key=True, index=True, default=generate_uuid)
    filename = Column(Text, nullable=False)
    doc_metadata = Column("metadata", JSON)
    content = Column(Text)
    embedding = Column(Vector(1536))
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")