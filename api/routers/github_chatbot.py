from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from ..services.github_chatbot_service import GitHubChatbotService
from ..services.github_service import GitHubService
from ..models.chatbot import ChatMessage, ChatResponse
from ..services.db import get_db, get_user_by_session_id
from api.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/github-chatbot", tags=["github-chatbot"])

SESSION_COOKIE = "mcp_session_id"

def get_github_chatbot_service() -> GitHubChatbotService:
    return GitHubChatbotService()

def get_github_service() -> GitHubService:
    return GitHubService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

@router.post("/chat")
def chat_with_github_assistant(
    request: Request,
    message: ChatMessage,
    chatbot_service: GitHubChatbotService = Depends(get_github_chatbot_service),
    github_service: GitHubService = Depends(get_github_service),
    db: Session = Depends(get_db)
) -> ChatResponse:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        github_data = github_service.get_all_github_data(user.github_access_token)
        response = chatbot_service.chat_about_github(message.message, github_data)
        return ChatResponse(
            response=response,
            status="success",
            message_count=len(github_data.get("repositories", []))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

@router.get("/suggestions")
def get_github_chat_suggestions() -> Dict:
    suggestions = [
        "How many repositories do I have?",
        "What are my most recent commits?",
        "Show me my open issues",
        "What languages do I use most?",
        "Which repositories are most active?",
        "How many pull requests do I have?",
        "What's my GitHub activity pattern?",
        "Which repositories have the most stars?",
        "What are my most popular repositories?",
        "Show me my recent contributions"
    ]
    return {"suggestions": suggestions} 