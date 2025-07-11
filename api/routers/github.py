from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict
from ..services.github_service import GitHubService
from ..services.github_auth_service import GitHubAuthService
from ..services.ai_service import AIService
from ..models.github import GitHubSummary
from ..utils import session_tokens

router = APIRouter(prefix="/github", tags=["github"])

def get_github_service() -> GitHubService:
    return GitHubService()

def get_github_auth_service() -> GitHubAuthService:
    return GitHubAuthService()

def get_ai_service() -> AIService:
    return AIService()

def is_github_authenticated(request: Request) -> bool:
    return bool(session_tokens.get_github_token(request))

@router.get("/login")
def github_login(request: Request, auth_service: GitHubAuthService = Depends(get_github_auth_service)):
    if is_github_authenticated(request):
        return {"message": "Already authenticated with GitHub"}
    auth_url = auth_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
def github_callback(request: Request, code: str, auth_service: GitHubAuthService = Depends(get_github_auth_service)):
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
        session_tokens.set_github_token(request, token_response["access_token"])
        return {"message": "GitHub authentication successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub authentication failed: {str(e)}")

@router.get("/status")
def github_auth_status(request: Request):
    if is_github_authenticated(request):
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
def github_logout(request: Request):
    session_tokens.clear_github_token(request)
    return {"message": "GitHub logout successful"}

@router.get("/summary")
def get_github_summary(request: Request, github_service: GitHubService = Depends(get_github_service)) -> GitHubSummary:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_github_summary(session_tokens.get_github_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get GitHub summary: {str(e)}")

@router.get("/repositories")
def get_github_repositories(request: Request, github_service: GitHubService = Depends(get_github_service)) -> List[Dict]:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_repositories(session_tokens.get_github_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repositories: {str(e)}")

@router.get("/commits")
def get_github_commits(request: Request, github_service: GitHubService = Depends(get_github_service)) -> List[Dict]:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        repositories = github_service.get_user_repositories(session_tokens.get_github_token(request))
        all_commits = []
        for repo in repositories[:10]:
            try:
                commits = github_service.get_repository_commits(
                    session_tokens.get_github_token(request),
                    repo["full_name"]
                )
                all_commits.extend(commits)
            except Exception as e:
                print(f"Warning: Could not get commits for {repo['full_name']}: {e}")
        return all_commits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commits: {str(e)}")

@router.get("/issues")
def get_github_issues(request: Request, github_service: GitHubService = Depends(get_github_service)) -> List[Dict]:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_issues(session_tokens.get_github_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get issues: {str(e)}")

@router.get("/pull-requests")
def get_github_pull_requests(request: Request, github_service: GitHubService = Depends(get_github_service)) -> List[Dict]:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        return github_service.get_user_pull_requests(session_tokens.get_github_token(request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pull requests: {str(e)}")

@router.get("/ai-summary")
def get_ai_github_summary(request: Request, github_service: GitHubService = Depends(get_github_service), ai_service: AIService = Depends(get_ai_service)) -> Dict:
    if not is_github_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    try:
        github_data = github_service.get_all_github_data(session_tokens.get_github_token(request))
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