from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ..services.teams_chatbot_service import TeamsChatbotService
from ..services.teams_service import TeamsService
from ..models.chatbot import ChatMessage, ChatResponse
from .teams import is_teams_authenticated, teams_tokens

router = APIRouter(prefix="/teams-chatbot", tags=["teams-chatbot"])

def get_teams_chatbot_service() -> TeamsChatbotService:
    """Dependency to get Teams chatbot service"""
    return TeamsChatbotService()

def get_teams_service() -> TeamsService:
    """Dependency to get Teams service"""
    return TeamsService()

@router.post("/chat")
def chat_with_teams_assistant(
    message: ChatMessage,
    chatbot_service: TeamsChatbotService = Depends(get_teams_chatbot_service),
    teams_service: TeamsService = Depends(get_teams_service)
) -> ChatResponse:
    """Chat with Teams assistant"""
    if not is_teams_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        # Get Teams data for context
        teams_data = teams_service.get_all_teams_data(teams_tokens["teams_access_token"])
        
        # Generate chatbot response
        response = chatbot_service.chat_about_teams(message.message, teams_data)
        
        return ChatResponse(
            response=response,
            status="success",
            message_count=len(teams_data.get("teams", []))
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

@router.get("/suggestions")
def get_teams_chat_suggestions() -> Dict:
    """Get suggested questions for the Teams chatbot"""
    suggestions = [
        "How many teams do I have?",
        "What are my most active channels?",
        "Show me recent messages from my teams",
        "Which teams have the most activity?",
        "What are my personal chat conversations?",
        "How many channels do I have access to?",
        "What's my Teams activity pattern?",
        "Which channels are most active?",
        "Show me messages from a specific team",
        "What are my recent conversations?",
        "What meetings do I have coming up?",
        "Show me my recent meetings",
        "How many online meetings do I have?",
        "Who are the organizers of my meetings?",
        "What's my meeting schedule like?"
    ]
    
    return {"suggestions": suggestions} 