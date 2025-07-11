from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Dict
from ..services.auth_service import AuthService
from ..models.auth import AuthStatus, TokenResponse, AuthError
from ..utils import session_tokens

router = APIRouter(prefix="/auth", tags=["authentication"])

def get_auth_service() -> AuthService:
    """Dependency to get auth service"""
    return AuthService()

def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated"""
    return bool(session_tokens.get_outlook_token(request))

@router.get("/login")
def login(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    """Redirect to Microsoft OAuth login"""
    if is_authenticated(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    
    auth_url = auth_service.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(request: Request, code: str, auth_service: AuthService = Depends(get_auth_service)):
    """Handle OAuth callback"""
    try:
        token_response = auth_service.get_access_token(code)
        
        if "error" in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"Authentication failed: {token_response.get('error_description', token_response['error'])}"
            )
        
        if "access_token" not in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"Authentication failed: No access token received. Response: {token_response}"
            )
        
        session_tokens.set_outlook_token(request, token_response["access_token"])
        
        return RedirectResponse(url="/dashboard", status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/status")
def auth_status(request: Request) -> AuthStatus:
    """Get authentication status"""
    if is_authenticated(request):
        return AuthStatus(
            is_authenticated=True,
            message="User is authenticated"
        )
    else:
        return AuthStatus(
            is_authenticated=False,
            message="User is not authenticated"
        )

@router.post("/logout")
def logout(request: Request):
    """Logout user"""
    session_tokens.clear_outlook_token(request)
    return {"message": "Logged out successfully"}

@router.get("/logout")
def logout_get(request: Request):
    """Logout user (GET version for browser links)"""
    session_tokens.clear_outlook_token(request)
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/token")
def get_token(request: Request) -> TokenResponse:
    """Get current access token (for API usage)"""
    token = session_tokens.get_outlook_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return TokenResponse(access_token=token) 