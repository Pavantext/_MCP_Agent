from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from ..services.github_chatbot_service import GitHubChatbotService
from ..services.github_service import GitHubService
from ..models.chatbot import ChatMessage, ChatResponse
from ..utils import session_tokens

router = APIRouter(prefix="/github-chatbot", tags=["github-chatbot"])

def get_github_chatbot_service() -> GitHubChatbotService:
    return GitHubChatbotService()

def get_github_service() -> GitHubService:
    return GitHubService()

@router.post("/chat")
def chat_with_github_assistant(
    request: Request,
    message: ChatMessage,
    chatbot_service: GitHubChatbotService = Depends(get_github_chatbot_service),
    github_service: GitHubService = Depends(get_github_service)
) -> ChatResponse:
    if not session_tokens.get_github_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        github_data = github_service.get_all_github_data(session_tokens.get_github_token(request))
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