from pydantic import BaseModel
from typing import Optional, List


class ChatMessage(BaseModel):
    """Model for chat messages"""
    message: str
    timestamp: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for chatbot responses"""
    response: str
    status: str = "success"
    message_count: Optional[int] = None


class ChatSession(BaseModel):
    """Model for chat session"""
    session_id: str
    messages: List[ChatMessage] = []
    email_count: int = 0
    unread_count: int = 0 