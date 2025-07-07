from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    """Response model for authentication token"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None


class AuthError(BaseModel):
    """Error response model for authentication"""
    error: str
    error_description: str


class EmailSummary(BaseModel):
    """Response model for email summary"""
    summary: str
    email_count: int
    status: str = "success"


class AuthStatus(BaseModel):
    """Response model for authentication status"""
    is_authenticated: bool
    message: str 