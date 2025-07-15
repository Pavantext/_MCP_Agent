from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
import uuid

from .routers import auth, emails, chatbot, github, github_chatbot, teams, teams_chatbot
from .services.email_service import EmailService
from .services.ai_service import AIService
from .services.db import get_db, get_user_by_session_id, create_or_update_user
from api.models.user import User
from sqlalchemy.orm import Session

# Constants
APP_TITLE = "MCP Outlook Reader API"
APP_DESCRIPTION = "A modular API service for reading and summarizing Outlook emails"
APP_VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8000
STATIC_DIR = "frontend/static"
TEMPLATES_DIR = "frontend/templates"

# Create FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Include routers
app.include_router(auth.router)
app.include_router(emails.router)
app.include_router(chatbot.router)
app.include_router(github.router)
app.include_router(github_chatbot.router)
app.include_router(teams.router)
app.include_router(teams_chatbot.router)

# Serve static files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

SESSION_COOKIE = "mcp_session_id"
SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "super-secret-key-change-me")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

def require_authenticated_user(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/auth/github/callback")
def github_callback(request: Request, code: str, db: Session = Depends(get_db)):
    try:
        from .services.github_auth_service import GitHubAuthService
        auth_service = GitHubAuthService()
        token_response = auth_service.get_access_token(code)
        if "error" in token_response:
            return _create_error_html_response(
                "GitHub Authentication Error",
                f"Failed to authenticate with GitHub: {token_response.get('error_description', token_response['error'])}"
            )
        session_id = request.session.get(SESSION_COOKIE)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session[SESSION_COOKIE] = session_id
        create_or_update_user(db, session_id, github_access_token=token_response["access_token"])
        response = RedirectResponse(url="/dashboard", status_code=302)
        return response
    except Exception as e:
        return _create_error_html_response(
            "GitHub Authentication Error",
            f"Failed to authenticate with GitHub: {str(e)}"
        )

@app.get("/auth/teams/callback")
def teams_callback(request: Request, code: str = None, error: str = None, error_description: str = None, db: Session = Depends(get_db)):
    try:
        if error:
            error_msg = error_description or error
            return _create_error_html_response(
                "Teams Authentication Error",
                f"OAuth error: {error_msg}"
            )
        if not code:
            return _create_error_html_response(
                "Teams Authentication Error",
                "No authorization code received from Microsoft. Please try again."
            )
        from .services.teams_auth_service import TeamsAuthService
        auth_service = TeamsAuthService()
        token_response = auth_service.get_access_token(code)
        if "error" in token_response:
            return _create_error_html_response(
                "Teams Authentication Error",
                f"Failed to authenticate with Teams: {token_response.get('error_description', token_response['error'])}"
            )
        session_id = request.session.get(SESSION_COOKIE)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session[SESSION_COOKIE] = session_id
        create_or_update_user(
            db,
            session_id,
            teams_access_token=token_response["access_token"],
            teams_refresh_token=token_response.get("refresh_token")
        )
        response = RedirectResponse(url="/dashboard", status_code=302)
        return response
    except Exception as e:
        return _create_error_html_response(
            "Teams Authentication Error",
            f"Failed to authenticate with Teams: {str(e)}"
        )

@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_authenticated_user(request, db)
    try:
        email_service = EmailService()
        ai_service = AIService()
        access_token = user.outlook_access_token
        if not access_token:
            return HTMLResponse(
                content=_create_error_html_response(
                    "Error",
                    "No Outlook access token found. Please authenticate with Outlook."
                ).body.decode(),
                status_code=401
            )
        try:
            emails = email_service.get_all_emails(access_token)
        except Exception as e:
            if "401" in str(e) or "Unauthorized" in str(e):
                return HTMLResponse(
                    content=_create_error_html_response(
                        "Error",
                        "Outlook token is invalid or expired. Please re-authenticate."
                    ).body.decode(),
                    status_code=401
                )
            raise
        ai_summary = ai_service.summarize_emails(emails)
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
        return HTMLResponse(
            content=_create_error_html_response(
                "Error",
                f"Failed to load email summary: {str(e)}"
            ).body.decode(),
            status_code=500
        )

@app.get("/api/docs")
def api_docs():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs", status_code=302)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": APP_TITLE}

def _create_error_html_response(title: str, error_message: str) -> HTMLResponse:
    """Create a standardized error HTML response"""
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #dc3545; text-align: center; }}
            .error {{ background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .back {{ text-align: center; margin-top: 30px; }}
            .back a {{ background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>❌ {title}</h1>
            <div class="error">
                <h2>An error occurred</h2>
                <p>{error_message}</p>
            </div>
            <div class="back">
                <a href="/dashboard">← Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """) 