from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ..services.chatbot_service import ChatbotService
from ..services.email_service import EmailService
from ..models.chatbot import ChatMessage, ChatResponse
from .auth import is_authenticated, tokens

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

def get_chatbot_service() -> ChatbotService:
    """Dependency to get chatbot service"""
    return ChatbotService()

def get_email_service() -> EmailService:
    """Dependency to get email service"""
    return EmailService()

@router.post("/chat")
def chat_with_assistant(
    message: ChatMessage,
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    email_service: EmailService = Depends(get_email_service)
) -> ChatResponse:
    """Chat with email assistant"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Get emails for context
        emails = email_service.get_all_emails(tokens["access_token"])
        
        # Generate chatbot response
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
    """Get suggested questions for the chatbot"""
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