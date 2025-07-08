from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..services.github_service import GitHubService
from ..services.github_auth_service import GitHubAuthService
from ..services.ai_service import AIService
from ..models.github import GitHubSummary
from .auth import is_authenticated

router = APIRouter(prefix="/github", tags=["github"])

# Global GitHub token storage (in production, use a proper database)
github_tokens = {}

def get_github_service() -> GitHubService:
    """Dependency to get GitHub service"""
    return GitHubService()

def get_github_auth_service() -> GitHubAuthService:
    """Dependency to get GitHub auth service"""
    return GitHubAuthService()

def get_ai_service() -> AIService:
    """Dependency to get AI service"""
    return AIService()

def is_github_authenticated() -> bool:
    """Check if user is authenticated with GitHub"""
    return "github_access_token" in github_tokens and github_tokens["github_access_token"]

@router.get("/login")
def github_login(auth_service: GitHubAuthService = Depends(get_github_auth_service)):
    """Redirect to GitHub OAuth login"""
    if is_github_authenticated():
        return {"message": "Already authenticated with GitHub"}
    
    auth_url = auth_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
def github_callback(
    code: str,
    auth_service: GitHubAuthService = Depends(get_github_auth_service)
):
    """Handle GitHub OAuth callback"""
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
        
        github_tokens["github_access_token"] = token_response["access_token"]
        
        return {"message": "GitHub authentication successful"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub authentication failed: {str(e)}")

@router.get("/status")
def github_auth_status():
    """Get GitHub authentication status"""
    if is_github_authenticated():
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
def github_logout():
    """Logout from GitHub"""
    if "github_access_token" in github_tokens:
        del github_tokens["github_access_token"]
    
    return {"message": "GitHub logout successful"}

@router.get("/summary")
def get_github_summary(
    github_service: GitHubService = Depends(get_github_service)
) -> GitHubSummary:
    """Get GitHub summary"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        return github_service.get_github_summary(github_tokens["github_access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get GitHub summary: {str(e)}")

@router.get("/repositories")
def get_github_repositories(
    github_service: GitHubService = Depends(get_github_service)
) -> List[Dict]:
    """Get GitHub repositories"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        return github_service.get_user_repositories(github_tokens["github_access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repositories: {str(e)}")

@router.get("/commits")
def get_github_commits(
    github_service: GitHubService = Depends(get_github_service)
) -> List[Dict]:
    """Get GitHub commits"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        # Get all repositories and their commits
        repositories = github_service.get_user_repositories(github_tokens["github_access_token"])
        all_commits = []
        
        for repo in repositories[:10]:  # Limit to first 10 repos
            try:
                commits = github_service.get_repository_commits(
                    github_tokens["github_access_token"], 
                    repo["full_name"]
                )
                all_commits.extend(commits)
            except Exception as e:
                print(f"Warning: Could not get commits for {repo['full_name']}: {e}")
        
        return all_commits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commits: {str(e)}")

@router.get("/issues")
def get_github_issues(
    github_service: GitHubService = Depends(get_github_service)
) -> List[Dict]:
    """Get GitHub issues"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        return github_service.get_user_issues(github_tokens["github_access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get issues: {str(e)}")

@router.get("/pull-requests")
def get_github_pull_requests(
    github_service: GitHubService = Depends(get_github_service)
) -> List[Dict]:
    """Get GitHub pull requests"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        return github_service.get_user_pull_requests(github_tokens["github_access_token"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pull requests: {str(e)}")

@router.get("/ai-summary")
def get_ai_github_summary(
    github_service: GitHubService = Depends(get_github_service),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict:
    """Get AI-powered GitHub summary"""
    if not is_github_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")
    
    try:
        github_data = github_service.get_all_github_data(github_tokens["github_access_token"])
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