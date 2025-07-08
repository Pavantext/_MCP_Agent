from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ..services.github_chatbot_service import GitHubChatbotService
from ..services.github_service import GitHubService
from ..models.chatbot import ChatMessage, ChatResponse
from .github import is_github_authenticated, github_tokens

router = APIRouter(prefix="/github-chatbot", tags=["github-chatbot"])

def get_github_chatbot_service() -> GitHubChatbotService:
    """Dependency to get GitHub chatbot service"""
    return GitHubChatbotService()

def get_github_service() -> GitHubService:
    """Dependency to get GitHub service"""
    return GitHubService()

@router.post("/chat")
def chat_with_github_assistant(
    message: ChatMessage,
    chatbot_service: GitHubChatbotService = Depends(get_github_chatbot_service),
    github_service: GitHubService = Depends(get_github_service)
) -> ChatResponse:
    """Chat with GitHub assistant"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        # Get GitHub data for context
        github_data = github_service.get_all_github_data(github_tokens["github_access_token"])
        
        # Generate chatbot response
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
    """Get suggested questions for the GitHub chatbot"""
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