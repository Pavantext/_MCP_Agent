from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.email_service import EmailService
from ..services.ai_service import AIService
from ..models.auth import EmailSummary
from ..utils import session_tokens

router = APIRouter(prefix="/emails", tags=["emails"])

def get_email_service() -> EmailService:
    return EmailService()

def get_ai_service() -> AIService:
    return AIService()

@router.get("/summary")
def get_email_summary(request: Request, email_service: EmailService = Depends(get_email_service)) -> EmailSummary:
    if not session_tokens.get_outlook_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_email_summary(session_tokens.get_outlook_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get email summary: {str(e)}")

@router.get("/all")
def get_all_emails(request: Request, email_service: EmailService = Depends(get_email_service)) -> List[Dict]:
    if not session_tokens.get_outlook_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_all_emails(session_tokens.get_outlook_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/unread")
def get_unread_emails(request: Request, email_service: EmailService = Depends(get_email_service)) -> List[Dict]:
    if not session_tokens.get_outlook_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return email_service.get_unread_emails(session_tokens.get_outlook_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/ai-summary")
def get_ai_email_summary(request: Request, email_service: EmailService = Depends(get_email_service), ai_service: AIService = Depends(get_ai_service)) -> Dict:
    if not session_tokens.get_outlook_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        emails = email_service.get_all_emails(session_tokens.get_outlook_token(request))
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
def mark_email_as_read(request: Request, email_id: str, email_service: EmailService = Depends(get_email_service)) -> Dict:
    if not session_tokens.get_outlook_token(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        success = email_service.mark_as_read(session_tokens.get_outlook_token(request), email_id)
        if success:
            return {"message": "Email marked as read"}
        else:
            raise HTTPException(status_code=400, detail="Failed to mark email as read")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark email as read: {str(e)}") 