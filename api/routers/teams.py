from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.teams_service import TeamsService
from ..services.teams_auth_service import TeamsAuthService
from ..services.ai_service import AIService
from ..models.teams import TeamsSummary
from ..services.db import get_db, get_user_by_session_id, create_or_update_user
from api.models.user import User
from sqlalchemy.orm import Session
import uuid

router = APIRouter(prefix="/teams", tags=["teams"])

SESSION_COOKIE = "mcp_session_id"

def get_teams_service() -> TeamsService:
    return TeamsService()

def get_teams_auth_service() -> TeamsAuthService:
    return TeamsAuthService()

def get_ai_service() -> AIService:
    return AIService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

def is_teams_authenticated(request: Request, db: Session) -> bool:
    user = get_current_user(request, db)
    return user is not None and user.teams_access_token is not None

@router.get("/login")
def teams_login(request: Request, auth_service: TeamsAuthService = Depends(get_teams_auth_service), db: Session = Depends(get_db)):
    if is_teams_authenticated(request, db):
        return {"message": "Already authenticated with Teams"}
    auth_url = auth_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
def teams_callback(request: Request, code: str, auth_service: TeamsAuthService = Depends(get_teams_auth_service), db: Session = Depends(get_db)):
    try:
        token_response = auth_service.get_access_token(code)
        if "error" in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"Teams authentication failed: {token_response.get('error_description', token_response['error'])}"
            )
        if "access_token" not in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"Teams authentication failed: No access token received. Response: {token_response}"
            )
        session_id = request.session.get(SESSION_COOKIE)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session[SESSION_COOKIE] = session_id
        create_or_update_user(db, session_id, teams_access_token=token_response["access_token"], teams_refresh_token=token_response.get("refresh_token"))
        return {"message": "Teams authentication successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teams authentication failed: {str(e)}")

@router.get("/status")
def teams_auth_status(request: Request, db: Session = Depends(get_db)):
    if is_teams_authenticated(request, db):
        return {
            "is_authenticated": True,
            "message": "User is authenticated with Teams"
        }
    else:
        return {
            "is_authenticated": False,
            "message": "User is not authenticated with Teams"
        }

@router.post("/logout")
def teams_logout(request: Request, db: Session = Depends(get_db)):
    session_id = request.session.get(SESSION_COOKIE)
    if session_id:
        user = get_user_by_session_id(db, session_id)
        if user:
            user.teams_access_token = None
            user.teams_refresh_token = None
            db.commit()
    return {"message": "Teams logout successful"}

@router.get("/summary")
def get_teams_summary(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> TeamsSummary:
    """Get Teams summary"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        return teams_service.get_teams_summary(user.teams_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Teams summary: {str(e)}")

@router.get("/teams")
def get_teams(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get user's teams"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        return teams_service.get_user_teams(user.teams_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")

@router.get("/channels")
def get_teams_channels(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get all channels from all teams"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        teams = teams_service.get_user_teams(user.teams_access_token)
        all_channels = []
        
        for team in teams:
            try:
                channels = teams_service.get_team_channels(
                    user.teams_access_token, 
                    team["id"]
                )
                for channel in channels:
                    channel["team_name"] = team["displayName"]
                    channel["team_id"] = team["id"]
                all_channels.extend(channels)
            except Exception as e:
                print(f"Warning: Could not get channels for team {team['displayName']}: {e}")
        
        return all_channels
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get channels: {str(e)}")

@router.get("/messages")
def get_teams_messages(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get recent messages from all teams and chats"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        # Get all teams and their messages
        teams = teams_service.get_user_teams(user.teams_access_token)
        all_messages = []
        
        for team in teams:
            try:
                channels = teams_service.get_team_channels(
                    user.teams_access_token, 
                    team["id"]
                )
                for channel in channels:
                    try:
                        messages = teams_service.get_channel_messages(
                            user.teams_access_token, 
                            team["id"], 
                            channel["id"]
                        )
                        for message in messages:
                            message["channel_name"] = channel["displayName"]
                            message["team_name"] = team["displayName"]
                        all_messages.extend(messages)
                    except Exception as e:
                        print(f"Warning: Could not get messages for channel {channel['displayName']}: {e}")
            except Exception as e:
                print(f"Warning: Could not get channels for team {team['displayName']}: {e}")
        
        # Get personal chats
        try:
            chats = teams_service.get_chats(user.teams_access_token)
            for chat in chats:
                try:
                    chat_messages = teams_service.get_chat_messages(
                        user.teams_access_token, 
                        chat["id"]
                    )
                    for message in chat_messages:
                        message["chat_name"] = chat.get("topic", "Personal Chat")
                        message["is_personal_chat"] = True
                    all_messages.extend(chat_messages)
                except Exception as e:
                    print(f"Warning: Could not get messages for chat {chat.get('topic', 'Unknown')}: {e}")
        except Exception as e:
            print(f"Warning: Could not get personal chats: {e}")
        
        return all_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")

@router.get("/meetings")
def get_teams_meetings(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get user's meetings"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        return teams_service.get_user_meetings(user.teams_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meetings: {str(e)}")

@router.get("/meetings/{meeting_id}")
def get_meeting_details(
    request: Request,
    meeting_id: str,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> Dict:
    """Get detailed information about a specific meeting"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        return teams_service.get_meeting_details(user.teams_access_token, meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meeting details: {str(e)}")

@router.get("/meetings/{meeting_id}/attendance")
def get_meeting_attendance(
    request: Request,
    meeting_id: str,
    teams_service: TeamsService = Depends(get_teams_service),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get attendance report for a meeting"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        return teams_service.get_meeting_attendance(user.teams_access_token, meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meeting attendance: {str(e)}")

@router.get("/ai-summary")
def get_ai_teams_summary(
    request: Request,
    teams_service: TeamsService = Depends(get_teams_service),
    ai_service: AIService = Depends(get_ai_service),
    db: Session = Depends(get_db)
) -> Dict:
    """Get AI-powered Teams summary"""
    if not is_teams_authenticated(request, db):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    
    try:
        user = get_current_user(request, db)
        teams_data = teams_service.get_all_teams_data(user.teams_access_token)
        meetings = teams_service.get_user_meetings(user.teams_access_token)
        teams_data["meetings"] = meetings
        teams_data["total_meetings"] = len(meetings)
        
        ai_summary = ai_service.summarize_teams_data(teams_data)
        
        return {
            "summary": ai_summary,
            "total_teams": teams_data["total_teams"],
            "total_channels": teams_data["total_channels"],
            "total_messages": teams_data["total_messages"],
            "total_chats": teams_data["total_chats"],
            "total_meetings": teams_data["total_meetings"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {str(e)}") 