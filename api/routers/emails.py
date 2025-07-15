from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.email_service import EmailService
from ..services.ai_service import AIService
from ..models.auth import EmailSummary
from ..services.db import get_db, get_user_by_session_id
from api.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/emails", tags=["emails"])

SESSION_COOKIE = "mcp_session_id"

def get_email_service() -> EmailService:
    return EmailService()

def get_ai_service() -> AIService:
    return AIService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

@router.get("/summary")
def get_email_summary(request: Request, email_service: EmailService = Depends(get_email_service), db: Session = Depends(get_db)) -> EmailSummary:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_email_summary(user.outlook_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get email summary: {str(e)}")

@router.get("/all")
def get_all_emails(request: Request, email_service: EmailService = Depends(get_email_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_all_emails(user.outlook_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/unread")
def get_unread_emails(request: Request, email_service: EmailService = Depends(get_email_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_unread_emails(user.outlook_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/ai-summary")
def get_ai_email_summary(request: Request, email_service: EmailService = Depends(get_email_service), ai_service: AIService = Depends(get_ai_service), db: Session = Depends(get_db)) -> Dict:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        emails = email_service.get_all_emails(user.outlook_access_token)
        ai_summary = ai_service.summarize_emails(emails)
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        return {
            "summary": ai_summary,
            "email_count": len(emails),
            "unread_count": unread_count,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {str(e)}")

@router.patch("/{email_id}/read")
def mark_email_as_read(email_id: str, request: Request, email_service: EmailService = Depends(get_email_service), db: Session = Depends(get_db)) -> Dict:
    user = get_current_user(request, db)
    if not user or not user.outlook_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        success = email_service.mark_as_read(user.outlook_access_token, email_id)
        if success:
            return {"message": "Email marked as read"}
        else:
            raise HTTPException(status_code=400, detail="Failed to mark email as read")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark email as read: {str(e)}") 