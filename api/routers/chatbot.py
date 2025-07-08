from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from ..services.chatbot_service import ChatbotService
from ..services.email_service import EmailService
from ..models.chatbot import ChatMessage, ChatResponse
from ..auth import get_current_user

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

def get_chatbot_service() -> ChatbotService:
    """Dependency to get chatbot service"""
    return ChatbotService()

def get_email_service() -> EmailService:
    """Dependency to get email service"""
    return EmailService()

@router.post("/chat")
async def chat_with_assistant(
    message: ChatMessage,
    request: Request,
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    email_service: EmailService = Depends(get_email_service),
    user: Dict = Depends(get_current_user)
) -> ChatResponse:
    """Chat with email assistant"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        # Get emails for context
        emails = email_service.get_all_emails(access_token)
        
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
async def get_chat_suggestions() -> Dict:
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