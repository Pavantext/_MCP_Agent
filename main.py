from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from auth import get_authorization_url, get_access_token
from outlook_api import get_unread_emails
from gemini import summarize_emails

app = FastAPI()
tokens = {}  # In-memory storage (use DB for real app)


@app.get("/")
def home():
    return {"message": "Welcome to MCP Outlook Reader! Go to /login to authenticate."}


@app.get("/login")
def login():
    return RedirectResponse(get_authorization_url())


@app.get("/auth/callback")
def callback(code: str):
    try:
        token_response = get_access_token(code)
        
        # Check if the response contains an error
        if "error" in token_response:
            return {"error": f"Authentication failed: {token_response.get('error_description', token_response['error'])}"}
        
        # Check if access_token exists in response
        if "access_token" not in token_response:
            return {"error": f"Authentication failed: No access token received. Response: {token_response}"}
        
        tokens["access_token"] = token_response["access_token"]
        return {"message": "Authentication successful. Now visit /summarize-emails"}
    except Exception as e:
        return {"error": f"Authentication failed: {str(e)}"}


@app.get("/summarize-emails")
def summarize():
    if "access_token" not in tokens:
        return {"error": "You must login first at /login"}
    emails = get_unread_emails(tokens["access_token"])
    summary = summarize_emails(emails)
    return {"summary": summary}
