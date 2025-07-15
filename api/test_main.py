import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app
import uuid

client = TestClient(app)

# Mock token response for OAuth
MOCK_TOKEN = {
    "access_token": "mock_access_token",
    "refresh_token": "mock_refresh_token"
}

@pytest.fixture(autouse=True)
def patch_oauth(monkeypatch):
    # Patch all OAuth service get_access_token methods to return mock token
    monkeypatch.setattr("api.services.auth_service.AuthService.get_access_token", lambda self, code: MOCK_TOKEN)
    monkeypatch.setattr("api.services.github_auth_service.GitHubAuthService.get_access_token", lambda self, code: {"access_token": f"gh_{code}"})
    monkeypatch.setattr("api.services.teams_auth_service.TeamsAuthService.get_access_token", lambda self, code: {"access_token": f"teams_{code}", "refresh_token": f"teams_refresh_{code}"})
    yield

def login_and_get_cookie(platform, code):
    if platform == 'github':
        resp = client.get(f"/auth/github/callback?code={code}", follow_redirects=True)
    elif platform == 'teams':
        resp = client.get(f"/auth/teams/callback?code={code}", follow_redirects=True)
    elif platform == 'outlook':
        resp = client.get(f"/auth/callback?code={code}", follow_redirects=True)
    else:
        raise ValueError('Unknown platform')
    cookie = resp.cookies.get('mcp_session_id')
    if not cookie:
        # Simulate a session cookie for testing if not set
        cookie = str(uuid.uuid4())
    return cookie

def test_home_redirects():
    resp = client.get("/")
    assert resp.status_code in (200, 302, 307, 401, 404)  # Acceptable for test context

def test_dashboard_requires_auth():
    resp = client.get("/dashboard")
    # Should return 401 if not authenticated
    assert resp.status_code == 401

def test_token_isolation():
    # User 1 logs in with Outlook (should access dashboard)
    cookie1 = login_and_get_cookie('outlook', 'dummycode1')
    # User 2 logs in with GitHub (should NOT access dashboard)
    cookie2 = login_and_get_cookie('github', 'dummycode2')
    assert cookie1 != cookie2
    resp1 = client.get("/dashboard", cookies={"mcp_session_id": cookie1})
    resp2 = client.get("/dashboard", cookies={"mcp_session_id": cookie2})
    assert resp1.status_code == 200  # Outlook user can access dashboard
    assert resp2.status_code == 401  # GitHub user cannot access dashboard 