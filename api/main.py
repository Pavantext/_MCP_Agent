from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

from .routers import auth, emails, chatbot
from .services.email_service import EmailService
from .services.ai_service import AIService
from .routers.auth import is_authenticated, tokens

# Create FastAPI app
app = FastAPI(
    title="MCP Outlook Reader API",
    description="A modular API service for reading and summarizing Outlook emails",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(emails.router)
app.include_router(chatbot.router)

# Serve static files
if os.path.exists("frontend/static"):
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
def home():
    """Main entry point - redirects based on authentication status"""
    if is_authenticated():
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/dashboard")
def dashboard(request: Request):
    """Main dashboard - shows email summary if authenticated"""
    if not is_authenticated():
        return RedirectResponse(url="/auth/login", status_code=302)
    
    try:
        email_service = EmailService()
        ai_service = AIService()
        
        emails = email_service.get_all_emails(tokens["access_token"])
        ai_summary = ai_service.summarize_emails(emails)
        
        # Count unread emails
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "summary": ai_summary,
                "email_count": len(emails),
                "unread_count": unread_count
            }
        )
        
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #dc3545; text-align: center; }}
                .error {{ background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .logout {{ text-align: center; margin-top: 30px; }}
                .logout a {{ background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Error</h1>
                <div class="error">
                    <h2>Failed to load email summary</h2>
                    <p>{str(e)}</p>
                </div>
                <div class="logout">
                    <a href="/auth/logout">🚪 Logout</a>
                </div>
            </div>
        </body>
        </html>
        """)

@app.get("/api/docs")
def api_docs():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs", status_code=302)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MCP Outlook Reader API"} 