from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.teams_service import TeamsService
from ..services.teams_auth_service import TeamsAuthService
from ..services.ai_service import AIService
from ..models.teams import TeamsSummary
from ..utils import session_tokens

router = APIRouter(prefix="/teams", tags=["teams"])

def get_teams_service() -> TeamsService:
    return TeamsService()

def get_teams_auth_service() -> TeamsAuthService:
    return TeamsAuthService()

def get_ai_service() -> AIService:
    return AIService()

def is_teams_authenticated(request: Request) -> bool:
    return bool(session_tokens.get_teams_token(request))

@router.get("/login")
def teams_login(request: Request, auth_service: TeamsAuthService = Depends(get_teams_auth_service)):
    if is_teams_authenticated(request):
        return {"message": "Already authenticated with Teams"}
    auth_url = auth_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
def teams_callback(request: Request, code: str, auth_service: TeamsAuthService = Depends(get_teams_auth_service)):
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
        session_tokens.set_teams_token(request, token_response["access_token"], token_response.get("refresh_token"))
        return {"message": "Teams authentication successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teams authentication failed: {str(e)}")

@router.get("/status")
def teams_auth_status(request: Request):
    if is_teams_authenticated(request):
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
def teams_logout(request: Request):
    session_tokens.clear_teams_token(request)
    return {"message": "Teams logout successful"}

@router.get("/summary")
def get_teams_summary(request: Request, teams_service: TeamsService = Depends(get_teams_service)) -> TeamsSummary:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        return teams_service.get_teams_summary(session_tokens.get_teams_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Teams summary: {str(e)}")

@router.get("/teams")
def get_teams(request: Request, teams_service: TeamsService = Depends(get_teams_service)) -> List[Dict]:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        return teams_service.get_user_teams(session_tokens.get_teams_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")

@router.get("/channels")
def get_teams_channels(request: Request, teams_service: TeamsService = Depends(get_teams_service)) -> List[Dict]:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        teams = teams_service.get_user_teams(session_tokens.get_teams_token(request))
        all_channels = []
        for team in teams:
            try:
                channels = teams_service.get_team_channels(
                    session_tokens.get_teams_token(request),
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
def get_teams_messages(request: Request, teams_service: TeamsService = Depends(get_teams_service)) -> List[Dict]:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        teams = teams_service.get_user_teams(session_tokens.get_teams_token(request))
        all_messages = []
        for team in teams:
            try:
                channels = teams_service.get_team_channels(
                    session_tokens.get_teams_token(request),
                    team["id"]
                )
                for channel in channels:
                    try:
                        messages = teams_service.get_channel_messages(
                            session_tokens.get_teams_token(request),
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
        try:
            chats = teams_service.get_chats(session_tokens.get_teams_token(request))
            for chat in chats:
                try:
                    chat_messages = teams_service.get_chat_messages(
                        session_tokens.get_teams_token(request),
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
def get_teams_meetings(request: Request, teams_service: TeamsService = Depends(get_teams_service)) -> List[Dict]:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        return teams_service.get_user_meetings(session_tokens.get_teams_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meetings: {str(e)}")

@router.get("/meetings/{meeting_id}")
def get_meeting_details(request: Request, meeting_id: str, teams_service: TeamsService = Depends(get_teams_service)) -> Dict:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        return teams_service.get_meeting_details(session_tokens.get_teams_token(request), meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meeting details: {str(e)}")

@router.get("/meetings/{meeting_id}/attendance")
def get_meeting_attendance(request: Request, meeting_id: str, teams_service: TeamsService = Depends(get_teams_service)) -> List[Dict]:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        return teams_service.get_meeting_attendance(session_tokens.get_teams_token(request), meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meeting attendance: {str(e)}")

@router.get("/ai-summary")
def get_ai_teams_summary(request: Request, teams_service: TeamsService = Depends(get_teams_service), ai_service: AIService = Depends(get_ai_service)) -> Dict:
    if not is_teams_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with Teams")
    try:
        teams_data = teams_service.get_all_teams_data(session_tokens.get_teams_token(request))
        ai_summary = ai_service.summarize_teams_data(teams_data)
        return {
            "summary": ai_summary,
            "total_teams": teams_data["total_teams"],
            "total_channels": teams_data["total_channels"],
            "total_messages": teams_data["total_messages"],
            "total_meetings": teams_data["total_meetings"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {str(e)}") 