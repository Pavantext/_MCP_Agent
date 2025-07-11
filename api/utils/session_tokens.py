from fastapi import Request

# Platform keys
OUTLOOK_KEY = 'outlook_access_token'
GITHUB_KEY = 'github_access_token'
TEAMS_KEY = 'teams_access_token'
TEAMS_REFRESH_KEY = 'teams_refresh_token'

# --- Outlook (Microsoft) ---
def set_outlook_token(request: Request, token: str):
    request.session[OUTLOOK_KEY] = token

def get_outlook_token(request: Request) -> str:
    return request.session.get(OUTLOOK_KEY)

def clear_outlook_token(request: Request):
    request.session.pop(OUTLOOK_KEY, None)

# --- GitHub ---
def set_github_token(request: Request, token: str):
    request.session[GITHUB_KEY] = token

def get_github_token(request: Request) -> str:
    return request.session.get(GITHUB_KEY)

def clear_github_token(request: Request):
    request.session.pop(GITHUB_KEY, None)

# --- Teams ---
def set_teams_token(request: Request, access_token: str, refresh_token: str = None):
    request.session[TEAMS_KEY] = access_token
    if refresh_token:
        request.session[TEAMS_REFRESH_KEY] = refresh_token

def get_teams_token(request: Request) -> str:
    return request.session.get(TEAMS_KEY)

def get_teams_refresh_token(request: Request) -> str:
    return request.session.get(TEAMS_REFRESH_KEY)

def clear_teams_token(request: Request):
    request.session.pop(TEAMS_KEY, None)
    request.session.pop(TEAMS_REFRESH_KEY, None) 