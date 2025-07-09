from pydantic import BaseModel
from typing import List, Dict, Optional

class TeamsAuthStatus(BaseModel):
    """Teams authentication status"""
    is_authenticated: bool
    message: str

class TeamsTokenResponse(BaseModel):
    """Teams token response"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

class TeamsError(BaseModel):
    """Teams authentication error"""
    error: str
    error_description: str

class TeamsSummary(BaseModel):
    """Teams summary response"""
    channels: List[Dict]
    messages: List[Dict]
    meetings: List[Dict]
    total_channels: int
    total_messages: int
    total_teams: int
    total_meetings: int
    summary: str

class TeamsMeeting(BaseModel):
    """Teams meeting model"""
    id: str
    subject: str
    start: str
    end: str
    organizer: str
    attendees: List[str]
    isOnlineMeeting: bool
    joinUrl: Optional[str] = None
    body: Optional[str] = None 