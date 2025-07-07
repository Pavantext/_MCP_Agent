import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import Dict, Optional
from ..models.auth import TokenResponse, AuthError

load_dotenv()

class AuthService:
    """Service for handling Microsoft OAuth authentication"""
    
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.scopes = os.getenv("SCOPES")
        
        # Validate required environment variables
        if not all([self.client_id, self.tenant_id, self.redirect_uri, self.scopes]):
            missing_vars = []
            if not self.client_id:
                missing_vars.append("CLIENT_ID")
            if not self.tenant_id:
                missing_vars.append("TENANT_ID")
            if not self.redirect_uri:
                missing_vars.append("REDIRECT_URI")
            if not self.scopes:
                missing_vars.append("SCOPES")
            
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    
    def get_authorization_url(self) -> str:
        """Generate Microsoft OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "response_mode": "query",
            "scope": self.scopes,
        }
        return f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize?{urlencode(params)}"
    
    def get_access_token(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token"""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "scope": self.scopes,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        
        # Only add client_secret if it's configured (for confidential clients)
        if self.client_secret and self.client_secret != "your_client_secret_here":
            data["client_secret"] = self.client_secret
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"Failed to get access token: {str(e)}"
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
        """Validate if a token is still valid"""
        try:
            # Make a simple API call to validate the token
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            return response.status_code == 200
        except:
            return False 