from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..services.email_service import EmailService
from ..services.ai_service import AIService
from ..models.auth import EmailSummary
from .auth import is_authenticated, tokens

router = APIRouter(prefix="/emails", tags=["emails"])

def get_email_service() -> EmailService:
    """Dependency to get email service"""
    return EmailService()

def get_ai_service() -> AIService:
    """Dependency to get AI service"""
    return AIService()

@router.get("/summary")
def get_email_summary(
    email_service: EmailService = Depends(get_email_service)
) -> EmailSummary:
    """Get email summary"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        return email_service.get_email_summary(tokens["access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get email summary: {str(e)}")

@router.get("/unread")
def get_unread_emails(
    email_service: EmailService = Depends(get_email_service)
) -> List[Dict]:
    """Get unread emails"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        return email_service.get_unread_emails(tokens["access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/ai-summary")
def get_ai_email_summary(
    email_service: EmailService = Depends(get_email_service),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict:
    """Get AI-powered email summary"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        emails = email_service.get_unread_emails(tokens["access_token"])
        ai_summary = ai_service.summarize_emails(emails)
        
        return {
            "summary": ai_summary,
            "email_count": len(emails),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {str(e)}")

@router.patch("/{email_id}/read")
def mark_email_as_read(
    email_id: str,
    email_service: EmailService = Depends(get_email_service)
) -> Dict:
    """Mark an email as read"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        success = email_service.mark_as_read(tokens["access_token"], email_id)
        if success:
            return {"message": "Email marked as read"}
        else:
            raise HTTPException(status_code=400, detail="Failed to mark email as read")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark email as read: {str(e)}") 