import os
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Microsoft OAuth Configuration
MICROSOFT_CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID')
MICROSOFT_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET')
MICROSOFT_REDIRECT_URI = os.getenv('MICROSOFT_REDIRECT_URI', 'http://localhost:8000/auth/callback')

# GitHub OAuth Configuration
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:8000/auth/github/callback')

def get_microsoft_auth_url() -> str:
    """Generate Microsoft OAuth URL"""
    return (
        "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
        f"client_id={MICROSOFT_CLIENT_ID}&"
        "response_type=code&"
        "redirect_uri=http://localhost:8000/auth/callback&"
        "scope=offline_access%20Mail.Read&"
        "response_mode=query"
    )

def get_github_auth_url() -> str:
    """Generate GitHub OAuth URL"""
    return (
        "https://github.com/login/oauth/authorize?"
        f"client_id={GITHUB_CLIENT_ID}&"
        "scope=repo,user,read:org&"
        "redirect_uri=http://localhost:8000/auth/github/callback"
    )

async def handle_microsoft_callback(code: str) -> Dict:
    """Handle Microsoft OAuth callback"""
    try:
        # Exchange code for access token
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        token_data = {
            "client_id": MICROSOFT_CLIENT_ID,
            "client_secret": MICROSOFT_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:8000/auth/callback"
        }
        
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        token_info = response.json()
        
        return {
            "access_token": token_info.get("access_token"),
            "refresh_token": token_info.get("refresh_token"),
            "expires_in": token_info.get("expires_in")
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exchanging code for token: {str(e)}")

async def handle_github_callback(code: str) -> Dict:
    """Handle GitHub OAuth callback"""
    try:
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": "http://localhost:8000/auth/github/callback"
        }
        
        headers = {
            "Accept": "application/json"
        }
        
        response = requests.post(token_url, data=token_data, headers=headers)
        response.raise_for_status()
        token_info = response.json()
        
        return {
            "access_token": token_info.get("access_token"),
            "token_type": token_info.get("token_type"),
            "scope": token_info.get("scope")
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exchanging code for token: {str(e)}")

def get_current_user(request: Request) -> Dict:
    """Get current authenticated user from session"""
    # Check for Microsoft authentication
    if request.session.get('access_token'):
        return {"authenticated": True, "service": "microsoft"}
    
    # Check for GitHub authentication
    if request.session.get('github_access_token'):
        return {"authenticated": True, "service": "github"}
    
    raise HTTPException(status_code=401, detail="Not authenticated")

def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated with any service"""
    return bool(request.session.get('access_token') or request.session.get('github_access_token')) 