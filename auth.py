import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = os.getenv("SCOPES")


def get_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": SCOPES,
    }
    return f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?{urlencode(params)}"


def get_access_token(auth_code):
    # Check if required environment variables are set
    if not all([CLIENT_ID, TENANT_ID, REDIRECT_URI, SCOPES]):
        missing_vars = []
        if not CLIENT_ID:
            missing_vars.append("CLIENT_ID")
        if not TENANT_ID:
            missing_vars.append("TENANT_ID")
        if not REDIRECT_URI:
            missing_vars.append("REDIRECT_URI")
        if not SCOPES:
            missing_vars.append("SCOPES")
        
        return {
            "error": "missing_environment_variables",
            "error_description": f"Missing environment variables: {', '.join(missing_vars)}"
        }
    
    # Debug: Print the values being used (remove in production)
    print(f"Debug - CLIENT_ID: {CLIENT_ID[:10]}..." if CLIENT_ID else "CLIENT_ID: None")
    print(f"Debug - TENANT_ID: {TENANT_ID}")
    print(f"Debug - REDIRECT_URI: {REDIRECT_URI}")
    print(f"Debug - SCOPES: {SCOPES}")
    print(f"Debug - CLIENT_SECRET: {'Set' if CLIENT_SECRET else 'Not set'}")
    
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    # Only add client_secret if it's configured (for confidential clients)
    if CLIENT_SECRET and CLIENT_SECRET != "your_client_secret_here":
        data["client_secret"] = CLIENT_SECRET
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
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
