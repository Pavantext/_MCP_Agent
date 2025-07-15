from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from ..services.teams_chatbot_service import TeamsChatbotService
from ..services.teams_service import TeamsService
from ..models.chatbot import ChatMessage, ChatResponse
from ..services.db import get_db, get_user_by_session_id
from api.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/teams-chatbot", tags=["teams-chatbot"])

SESSION_COOKIE = "mcp_session_id"

def get_teams_chatbot_service() -> TeamsChatbotService:
    return TeamsChatbotService()

def get_teams_service() -> TeamsService:
    return TeamsService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

@router.post("/chat")
def chat_with_teams_assistant(
    request: Request,
    message: ChatMessage,
    chatbot_service: TeamsChatbotService = Depends(get_teams_chatbot_service),
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> ChatResponse:
    user = get_current_user(request, db)
    if not user or not user.teams_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        teams_data = teams_service.get_all_teams_data(user.teams_access_token)
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