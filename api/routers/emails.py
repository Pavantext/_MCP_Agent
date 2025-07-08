from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from typing import List, Dict
from ..services.email_service import EmailService
from ..services.ai_service import AIService
from ..models.auth import EmailSummary
from ..auth import get_current_user
from ..utils import read_template_file, safe_format

router = APIRouter(prefix="/emails", tags=["emails"])

def get_email_service() -> EmailService:
    """Dependency to get email service"""
    return EmailService()

def get_ai_service() -> AIService:
    """Dependency to get AI service"""
    return AIService()

@router.get("/dashboard", response_class=HTMLResponse)
async def email_dashboard(request: Request, user: Dict = Depends(get_current_user)):
    """Email dashboard page"""
    try:
        # Get access token from session
        access_token = request.session.get('access_token')
        if not access_token:
            return HTMLResponse("""
                <html>
                <head><title>Authentication Required</title></head>
                <body>
                    <h1>Authentication Required</h1>
                    <p>Please authenticate with Microsoft first.</p>
                    <a href="/auth">Connect Microsoft Account</a>
                </body>
                </html>
            """)
        
        # Get email service
        email_service = get_email_service()
        ai_service = get_ai_service()
        
        # Get emails and generate summary
        emails = email_service.get_all_emails(access_token)
        ai_summary = ai_service.summarize_emails(emails)
        
        # Count statistics
        email_count = len(emails)
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        
        # Render dashboard template using utility function
        template = read_template_file("frontend/templates/dashboard.html")
        
        return HTMLResponse(safe_format(template,
            summary=ai_summary,
            email_count=email_count,
            unread_count=unread_count
        ))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading email dashboard: {str(e)}")

@router.get("/summary")
async def get_email_summary(
    request: Request,
    email_service: EmailService = Depends(get_email_service),
    user: Dict = Depends(get_current_user)
) -> EmailSummary:
    """Get email summary"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return email_service.get_email_summary(access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get email summary: {str(e)}")

@router.get("/all")
async def get_all_emails(
    request: Request,
    email_service: EmailService = Depends(get_email_service),
    user: Dict = Depends(get_current_user)
) -> List[Dict]:
    """Get all emails"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return email_service.get_all_emails(access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/unread")
async def get_unread_emails(
    request: Request,
    email_service: EmailService = Depends(get_email_service),
    user: Dict = Depends(get_current_user)
) -> List[Dict]:
    """Get unread emails"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return email_service.get_unread_emails(access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@router.get("/ai-summary")
async def get_ai_email_summary(
    request: Request,
    email_service: EmailService = Depends(get_email_service),
    ai_service: AIService = Depends(get_ai_service),
    user: Dict = Depends(get_current_user)
) -> Dict:
    """Get AI-powered email summary"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        emails = email_service.get_all_emails(access_token)
        ai_summary = ai_service.summarize_emails(emails)
        
        # Count unread emails
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
async def mark_email_as_read(
    email_id: str,
    request: Request,
    email_service: EmailService = Depends(get_email_service),
    user: Dict = Depends(get_current_user)
) -> Dict:
    """Mark an email as read"""
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        success = email_service.mark_as_read(access_token, email_id)
        if success:
            return {"message": "Email marked as read"}
        else:
            raise HTTPException(status_code=400, detail="Failed to mark email as read")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark email as read: {str(e)}") 