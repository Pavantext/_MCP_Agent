from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from typing import Dict
from ..services.auth_service import AuthService
from ..models.auth import AuthStatus, TokenResponse, AuthError

router = APIRouter(prefix="/auth", tags=["authentication"])

# Global token storage (in production, use a proper database)
tokens = {}

def get_auth_service() -> AuthService:
    """Dependency to get auth service"""
    return AuthService()

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return "access_token" in tokens and tokens["access_token"]

@router.get("/login")
def login(auth_service: AuthService = Depends(get_auth_service)):
    """Redirect to Microsoft OAuth login"""
    if is_authenticated():
        return RedirectResponse(url="/dashboard", status_code=302)
    
    auth_url = auth_service.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(
    code: str,
    auth_service: AuthService = Depends(get_auth_service)
):
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
        
        tokens["access_token"] = token_response["access_token"]
        
        return RedirectResponse(url="/dashboard", status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/status")
def auth_status() -> AuthStatus:
    """Get authentication status"""
    if is_authenticated():
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
def logout():
    """Logout user"""
    if "access_token" in tokens:
        del tokens["access_token"]
    
    return {"message": "Logged out successfully"}

@router.get("/token")
def get_token() -> TokenResponse:
    """Get current access token (for API usage)"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return TokenResponse(access_token=tokens["access_token"]) 