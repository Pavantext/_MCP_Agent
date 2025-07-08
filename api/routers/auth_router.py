from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from ..auth import (
    get_microsoft_auth_url, handle_microsoft_callback,
    get_github_auth_url, handle_github_callback,
    get_current_user, is_authenticated
)
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/")
async def auth_home(request: Request):
    """Show authentication options"""
    if is_authenticated(request):
        return RedirectResponse(url="/dashboard")
    
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Choose Service</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    text-align: center;
                    max-width: 500px;
                    width: 90%;
                }
                
                h1 {
                    color: #333;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    font-weight: 600;
                }
                
                .service-options {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }
                
                .service-btn {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    padding: 20px;
                    border: none;
                    border-radius: 12px;
                    font-size: 1.1em;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    color: white;
                }
                
                .outlook-btn {
                    background: #0078d4;
                }
                
                .outlook-btn:hover {
                    background: #106ebe;
                    transform: translateY(-2px);
                }
                
                .github-btn {
                    background: #24292e;
                }
                
                .github-btn:hover {
                    background: #586069;
                    transform: translateY(-2px);
                }
                
                .service-icon {
                    font-size: 1.5em;
                }
                
                .description {
                    color: #666;
                    margin-top: 20px;
                    font-size: 0.9em;
                    line-height: 1.5;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Choose Your Service</h1>
                <div class="service-options">
                    <a href="/auth/microsoft" class="service-btn outlook-btn">
                        <span class="service-icon">📧</span>
                        <span>Outlook Email</span>
                    </a>
                    <a href="/auth/github-auth" class="service-btn github-btn">
                        <span class="service-icon">🐙</span>
                        <span>GitHub</span>
                    </a>
                </div>
                <div class="description">
                    Select a service to connect and view your data with AI-powered insights
                </div>
            </div>
        </body>
        </html>
    """)

@router.get("/microsoft")
async def microsoft_auth():
    """Redirect to Microsoft OAuth"""
    auth_url = get_microsoft_auth_url()
    return RedirectResponse(url=auth_url)

@router.get("/github-auth")
async def github_auth():
    """Redirect to GitHub OAuth"""
    auth_url = get_github_auth_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def microsoft_callback(code: str, request: Request):
    """Handle Microsoft OAuth callback"""
    try:
        token_info = await handle_microsoft_callback(code)
        
        # Store tokens in session
        request.session['access_token'] = token_info['access_token']
        if 'refresh_token' in token_info:
            request.session['refresh_token'] = token_info['refresh_token']
        
        return RedirectResponse(url="/dashboard")
        
    except Exception as e:
        return HTMLResponse(f"""
            <html>
            <head><title>Authentication Error</title></head>
            <body>
                <h1>Authentication Error</h1>
                <p>{str(e)}</p>
                <a href="/auth">Try Again</a>
            </body>
            </html>
        """)

@router.get("/github/callback")
async def github_callback(code: str, request: Request):
    """Handle GitHub OAuth callback"""
    try:
        token_info = await handle_github_callback(code)
        
        # Store tokens in session
        request.session['github_access_token'] = token_info['access_token']
        request.session['github_token_type'] = token_info.get('token_type', 'bearer')
        
        return RedirectResponse(url="/github/dashboard")
        
    except Exception as e:
        return HTMLResponse(f"""
            <html>
            <head><title>Authentication Error</title></head>
            <body>
                <h1>Authentication Error</h1>
                <p>{str(e)}</p>
                <a href="/auth">Try Again</a>
            </body>
            </html>
        """)

@router.get("/logout")
async def logout(request: Request):
    """Logout user"""
    # Clear all session data
    request.session.clear()
    return RedirectResponse(url="/auth")

@router.get("/status")
async def auth_status(request: Request):
    """Get authentication status"""
    if is_authenticated(request):
        user = get_current_user(request)
        return {"authenticated": True, "service": user.get("service")}
    return {"authenticated": False} 