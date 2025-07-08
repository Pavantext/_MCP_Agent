import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import Dict, Optional
from ..models.github import GitHubTokenResponse, GitHubError

load_dotenv()

class GitHubAuthService:
    """Service for handling GitHub OAuth authentication"""
    
    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/github/callback")
        self.scopes = os.getenv("GITHUB_SCOPES", "repo user")
        
        # Validate required environment variables
        if not self.client_id:
            raise ValueError("Missing environment variable: GITHUB_CLIENT_ID")
        if not self.client_secret:
            raise ValueError("Missing environment variable: GITHUB_CLIENT_SECRET")
    
    def get_authorization_url(self) -> str:
        """Generate GitHub OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "response_type": "code",
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    
    def get_access_token(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token"""
        url = "https://github.com/login/oauth/access_token"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"Failed to get GitHub access token: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_json = e.response.json()
                    error_detail += f" - {error_json.get('error_description', '')}"
                except:
                    error_detail += f" - Status: {e.response.status_code}"
            
            return {
                "error": "request_failed",
                "error_description": error_detail
            }
    
    def validate_token(self, token: str) -> bool:
        """Validate if a GitHub token is still valid"""
        try:
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, token: str) -> Dict:
        """Get GitHub user information"""
        try:
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get user info: {str(e)}") 