from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict
from ..services.auth_service import AuthService
from ..models.auth import AuthStatus, TokenResponse, AuthError
from ..services.db import get_db, get_user_by_session_id, create_or_update_user
from api.models.user import User
import uuid

router = APIRouter(prefix="/auth", tags=["authentication"])

SESSION_COOKIE = "mcp_session_id"

def get_auth_service() -> AuthService:
    return AuthService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

def is_authenticated(request: Request, db: Session = Depends(get_db)) -> bool:
    user = get_current_user(request, db)
    return user is not None and user.outlook_access_token is not None

@router.get("/login")
def login(request: Request, auth_service: AuthService = Depends(get_auth_service), db: Session = Depends(get_db)):
    if is_authenticated(request, db):
        return RedirectResponse(url="/dashboard", status_code=302)
    auth_url = auth_service.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(request: Request, code: str, auth_service: AuthService = Depends(get_auth_service), db: Session = Depends(get_db)):
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
        session_id = request.session.get(SESSION_COOKIE)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session[SESSION_COOKIE] = session_id
        create_or_update_user(db, session_id, outlook_access_token=token_response["access_token"], outlook_refresh_token=token_response.get("refresh_token"))
        return RedirectResponse(url="/dashboard", status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/status")
def auth_status(request: Request, db: Session = Depends(get_db)) -> AuthStatus:
    if is_authenticated(request, db):
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
def logout(request: Request, db: Session = Depends(get_db)):
    session_id = request.session.get(SESSION_COOKIE)
    if session_id:
        user = get_user_by_session_id(db, session_id)
        if user:
            user.outlook_access_token = None
            user.outlook_refresh_token = None
            user.github_access_token = None
            user.teams_access_token = None
            user.teams_refresh_token = None
            db.commit()
    return {"message": "Logged out successfully"}

@router.get("/token")
def get_token(request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return TokenResponse(access_token=user.outlook_access_token) 