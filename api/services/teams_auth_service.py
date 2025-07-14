import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import Dict, Optional
from ..models.teams import TeamsTokenResponse, TeamsError

load_dotenv()

class TeamsAuthService:
    """Service for handling Microsoft Teams OAuth authentication"""
    
    def __init__(self):
        self.client_id = os.getenv("TEAMS_CLIENT_ID")
        self.client_secret = os.getenv("TEAMS_CLIENT_SECRET")
        self.redirect_uri = os.getenv("TEAMS_REDIRECT_URI")
        self.scopes = os.getenv("TEAMS_SCOPES")
        self.tenant_id = os.getenv("TEAMS_TENANT_ID")
        
        # Microsoft Graph API endpoints
        # Use tenant-specific endpoint instead of /common for single-tenant apps
        self.auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize"
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        # Validate required environment variables
        if not self.client_id:
            raise ValueError("Missing environment variable: TEAMS_CLIENT_ID")
        if not self.client_secret:
            raise ValueError("Missing environment variable: TEAMS_CLIENT_SECRET")
    
    def get_authorization_url(self) -> str:
        """Generate Microsoft Teams OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "response_type": "code",
            "response_mode": "query"
        }
        return f"{self.auth_url}?{urlencode(params)}"
    
    def get_access_token(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token"""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        
        print(f"Teams token request - URL: {self.token_url}")
        print(f"Teams token request - Client ID: {self.client_id}")
        print(f"Teams token request - Redirect URI: {self.redirect_uri}")
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            print(f"Teams token response status: {response.status_code}")
            print(f"Teams token response: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"Failed to get Teams access token: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_json = e.response.json()
                    error_detail += f" - {error_json.get('error_description', '')}"
                except:
                    error_detail += f" - Status: {e.response.status_code}"
            
            print(f"Teams token error: {error_detail}")
            return {
                "error": "request_failed",
                "error_description": error_detail
            }
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        """Refresh access token using refresh token"""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"Failed to refresh Teams access token: {str(e)}"
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
        """Validate if a Teams token is still valid"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, token: str) -> Dict:
        """Get Microsoft Teams user information"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get user info: {str(e)}") 