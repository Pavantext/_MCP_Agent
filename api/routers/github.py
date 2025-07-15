from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.github_service import GitHubService
from ..services.github_auth_service import GitHubAuthService
from ..services.ai_service import AIService
from ..models.github import GitHubSummary
from ..services.db import get_db, get_user_by_session_id, create_or_update_user
from api.models.user import User
from sqlalchemy.orm import Session
import uuid

router = APIRouter(prefix="/github", tags=["github"])

SESSION_COOKIE = "mcp_session_id"

def get_github_service() -> GitHubService:
    return GitHubService()

def get_github_auth_service() -> GitHubAuthService:
    return GitHubAuthService()

def get_ai_service() -> AIService:
    return AIService()

def get_current_user(request: Request, db: Session):
    session_id = request.session.get(SESSION_COOKIE)
    if not session_id:
        return None
    return get_user_by_session_id(db, session_id)

def is_github_authenticated(request: Request, db: Session) -> bool:
    user = get_current_user(request, db)
    return user is not None and user.github_access_token is not None

@router.get("/login")
def github_login(request: Request, auth_service: GitHubAuthService = Depends(get_github_auth_service), db: Session = Depends(get_db)):
    if is_github_authenticated(request, db):
        return {"message": "Already authenticated with GitHub"}
    auth_url = auth_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
def github_callback(request: Request, code: str, auth_service: GitHubAuthService = Depends(get_github_auth_service), db: Session = Depends(get_db)):
    try:
        token_response = auth_service.get_access_token(code)
        if "error" in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"GitHub authentication failed: {token_response.get('error_description', token_response['error'])}"
            )
        if "access_token" not in token_response:
            raise HTTPException(
                status_code=400,
                detail=f"GitHub authentication failed: No access token received. Response: {token_response}"
            )
        session_id = request.session.get(SESSION_COOKIE)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session[SESSION_COOKIE] = session_id
        create_or_update_user(db, session_id, github_access_token=token_response["access_token"])
        return {"message": "GitHub authentication successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub authentication failed: {str(e)}")

@router.get("/status")
def github_auth_status(request: Request, db: Session = Depends(get_db)):
    if is_github_authenticated(request, db):
        return {
            "is_authenticated": True,
            "message": "User is authenticated with GitHub"
        }
    else:
        return {
            "is_authenticated": False,
            "message": "User is not authenticated with GitHub"
        }

@router.post("/logout")
def github_logout(request: Request, db: Session = Depends(get_db)):
    session_id = request.session.get(SESSION_COOKIE)
    if session_id:
        user = get_user_by_session_id(db, session_id)
        if user:
            user.github_access_token = None
            db.commit()
    return {"message": "GitHub logout successful"}

@router.get("/summary")
def get_github_summary(request: Request, github_service: GitHubService = Depends(get_github_service), db: Session = Depends(get_db)) -> GitHubSummary:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_github_summary(user.github_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get GitHub summary: {str(e)}")

@router.get("/repositories")
def get_github_repositories(request: Request, github_service: GitHubService = Depends(get_github_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_repositories(user.github_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repositories: {str(e)}")

@router.get("/commits")
def get_github_commits(request: Request, github_service: GitHubService = Depends(get_github_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        repositories = github_service.get_user_repositories(user.github_access_token)
        all_commits = []
        for repo in repositories[:10]:
            try:
                commits = github_service.get_repository_commits(
                    user.github_access_token,
                    repo["full_name"]
                )
                all_commits.extend(commits)
            except Exception as e:
                print(f"Warning: Could not get commits for {repo['full_name']}: {e}")
        return all_commits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commits: {str(e)}")

@router.get("/issues")
def get_github_issues(request: Request, github_service: GitHubService = Depends(get_github_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_issues(user.github_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get issues: {str(e)}")

@router.get("/pull-requests")
def get_github_pull_requests(request: Request, github_service: GitHubService = Depends(get_github_service), db: Session = Depends(get_db)) -> List[Dict]:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_pull_requests(user.github_access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pull requests: {str(e)}")

@router.get("/ai-summary")
def get_ai_github_summary(request: Request, github_service: GitHubService = Depends(get_github_service), ai_service: AIService = Depends(get_ai_service), db: Session = Depends(get_db)) -> Dict:
    user = get_current_user(request, db)
    if not user or not user.github_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        github_data = github_service.get_all_github_data(user.github_access_token)
        ai_summary = ai_service.summarize_github_data(github_data)
        return {
            "summary": ai_summary,
            "total_repos": github_data["total_repos"],
            "total_commits": github_data["total_commits"],
            "total_issues": github_data["total_issues"],
            "total_pull_requests": github_data["total_pull_requests"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {str(e)}") 