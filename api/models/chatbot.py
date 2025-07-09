from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    """Model for chat messages"""
    message: str
    timestamp: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for chatbot responses"""
    response: str
    status: str = "success"
    message_count: Optional[int] = None 