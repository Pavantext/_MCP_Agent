from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from starlette.middleware.sessions import SessionMiddleware

from .routers import auth, emails, chatbot, github, github_chatbot, teams, teams_chatbot
from .services.email_service import EmailService
from .services.ai_service import AIService
from .routers.auth import is_authenticated
from .utils import session_tokens

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
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SESSION_SECRET_KEY', 'super-secret-key'))

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

@app.get("/")
def home(request: Request):
    """Main entry point - redirects based on authentication status"""
    if is_authenticated(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/auth/github/callback")
def github_callback(code: str):
    """Handle GitHub OAuth callback"""
    try:
        from .services.github_auth_service import GitHubAuthService
        auth_service = GitHubAuthService()
        token_response = auth_service.get_access_token(code)
        
        if "error" in token_response:
            return _create_error_html_response(
                "GitHub Authentication Error",
                f"Failed to authenticate with GitHub: {token_response.get('error_description', token_response['error'])}"
            )
        
        # Store the token (in production, use a proper database)
        from .routers.github import github_tokens
        github_tokens["github_access_token"] = token_response["access_token"]
        
        return RedirectResponse(url="/dashboard", status_code=302)
        
    except Exception as e:
        return _create_error_html_response(
            "GitHub Authentication Error",
            f"Failed to authenticate with GitHub: {str(e)}"
        )

@app.get("/auth/teams/callback")
def teams_callback(code: str = None, error: str = None, error_description: str = None):
    """Handle Teams OAuth callback"""
    try:
        # Debug logging
        print(f"Teams callback received - code: {code}, error: {error}, error_description: {error_description}")
        
        # Check for OAuth errors first
        if error:
            error_msg = error_description or error
            print(f"Teams OAuth error: {error_msg}")
            return _create_error_html_response(
                "Teams Authentication Error",
                f"OAuth error: {error_msg}"
            )
        
        # Check if code is provided
        if not code:
            print("Teams callback: No authorization code received")
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
        
        # Store the token (in production, use a proper database)
        from .routers.teams import teams_tokens
        teams_tokens["teams_access_token"] = token_response["access_token"]
        if "refresh_token" in token_response:
            teams_tokens["teams_refresh_token"] = token_response["refresh_token"]
        
        return RedirectResponse(url="/dashboard", status_code=302)
        
    except Exception as e:
        return _create_error_html_response(
            "Teams Authentication Error",
            f"Failed to authenticate with Teams: {str(e)}"
        )

@app.get("/dashboard")
def dashboard(request: Request):
    """Main dashboard - shows email summary if authenticated"""
    if not is_authenticated(request):
        return RedirectResponse(url="/auth/login", status_code=302)
    try:
        email_service = EmailService()
        ai_service = AIService()
        access_token = session_tokens.get_outlook_token(request)
        emails = email_service.get_all_emails(access_token)
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
        return _create_error_html_response(
            "Error",
            f"Failed to load email summary: {str(e)}"
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