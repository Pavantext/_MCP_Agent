from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from ..services.chatbot_service import ChatbotService
from ..services.email_service import EmailService
from ..models.chatbot import ChatMessage, ChatResponse
from ..services.db import get_db, get_user_by_session_id
from api.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

SESSION_COOKIE = "mcp_session_id"

def get_chatbot_service() -> ChatbotService:
    return ChatbotService()

def get_email_service() -> EmailService:
    return EmailService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

@router.post("/chat")
def chat_with_assistant(
    request: Request,
    message: ChatMessage,
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    email_service: EmailService = Depends(get_email_service),
    db: Session = Depends(get_db)
) -> ChatResponse:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        emails = email_service.get_all_emails(user.outlook_access_token)
        response = chatbot_service.chat_about_emails(message.message, emails)
        return ChatResponse(
            response=response,
            status="success",
            message_count=len(emails)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

@router.get("/suggestions")
def get_chat_suggestions() -> Dict:
    suggestions = [
        "How many unread emails do I have?",
        "Show me emails from a specific sender",
        "What are the most recent emails?",
        "Are there any urgent emails?",
        "Summarize my emails by topic",
        "Find emails about meetings",
        "What's my email activity pattern?",
        "Which senders email me most often?"
    ]
    return {"suggestions": suggestions} 