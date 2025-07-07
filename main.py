from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from auth import get_authorization_url, get_access_token
from outlook_api import get_unread_emails
from gemini import summarize_emails
import json

app = FastAPI()
tokens = {}  # In-memory storage (use DB for real app)


def is_authenticated():
    """Check if user is authenticated"""
    return "access_token" in tokens and tokens["access_token"]


@app.get("/")
def home():
    """Main entry point - redirects based on authentication status"""
    if is_authenticated():
        # User is authenticated, redirect to email summary
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        # User is not authenticated, redirect to login
        return RedirectResponse(url="/login", status_code=302)


@app.get("/login")
def login():
    """Redirect to Microsoft OAuth login"""
    if is_authenticated():
        # User is already authenticated, redirect to dashboard
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(get_authorization_url())


@app.get("/auth/callback")
def callback(code: str):
    """Handle OAuth callback and redirect to dashboard"""
    try:
        token_response = get_access_token(code)
        
        # Check if the response contains an error
        if "error" in token_response:
            return {"error": f"Authentication failed: {token_response.get('error_description', token_response['error'])}"}
        
        # Check if access_token exists in response
        if "access_token" not in token_response:
            return {"error": f"Authentication failed: No access token received. Response: {token_response}"}
        
        tokens["access_token"] = token_response["access_token"]
        
        # Redirect to dashboard after successful authentication
        return RedirectResponse(url="/dashboard", status_code=302)
        
    except Exception as e:
        return {"error": f"Authentication failed: {str(e)}"}


@app.get("/dashboard")
def dashboard():
    """Main dashboard - shows email summary if authenticated"""
    if not is_authenticated():
        # User is not authenticated, redirect to login
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        emails = get_unread_emails(tokens["access_token"])
        summary = summarize_emails(emails)
        
        # Return a nice HTML response with the summary
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Summary Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; }}
                .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .logout {{ text-align: center; margin-top: 30px; }}
                .logout a {{ background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
                .logout a:hover {{ background: #c82333; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📧 Email Summary Dashboard</h1>
                <div class="summary">
                    <h2>📋 Summary</h2>
                    <pre>{summary}</pre>
                </div>
                <div class="logout">
                    <a href="/logout">🚪 Logout</a>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        return {"error": f"Failed to get email summary: {str(e)}"}


@app.get("/logout")
def logout():
    """Logout user and redirect to home"""
    # Clear the access token
    if "access_token" in tokens:
        del tokens["access_token"]
    
    # Redirect to home page
    return RedirectResponse(url="/", status_code=302)


@app.get("/summarize-emails")
def summarize():
    """Legacy endpoint - redirects to dashboard"""
    if not is_authenticated():
        return {"error": "You must login first at /login"}
    return RedirectResponse(url="/dashboard", status_code=302)
