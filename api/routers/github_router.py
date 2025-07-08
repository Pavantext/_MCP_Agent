from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from ..services.github_service import GitHubService
from ..services.github_ai_service import GitHubAIService
from ..services.github_chatbot_service import GitHubChatbotService
from ..models.github import GitHubSummary
from ..auth import get_current_user
from ..utils import read_template_file, safe_format
from typing import Dict, List
import json
import traceback

router = APIRouter(prefix="/github", tags=["GitHub"])

github_service = GitHubService()
github_ai_service = GitHubAIService()
github_chatbot_service = GitHubChatbotService()

@router.get("/test")
async def test_github_auth(request: Request):
    """Test GitHub authentication"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            return {"status": "not_authenticated", "message": "No GitHub token found"}
        
        # Test user info
        user_info = github_service.get_user_info(github_token)
        if user_info:
            return {
                "status": "authenticated",
                "user": user_info.get('login', 'Unknown'),
                "token_preview": f"{github_token[:10]}...",
                "message": "GitHub authentication working"
            }
        else:
            return {"status": "error", "message": "Could not fetch user info"}
            
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

@router.get("/dashboard", response_class=HTMLResponse)
async def github_dashboard(request: Request, user: Dict = Depends(get_current_user)):
    """GitHub dashboard page"""
    try:
        # Get GitHub access token from session
        github_token = request.session.get('github_access_token')
        if not github_token:
            return HTMLResponse("""
                <html>
                <head><title>GitHub Authentication Required</title></head>
                <body>
                    <h1>GitHub Authentication Required</h1>
                    <p>Please authenticate with GitHub first.</p>
                    <a href="/auth/github">Connect GitHub Account</a>
                </body>
                </html>
            """)
        
        print(f"GitHub token found: {github_token[:10]}...")
        
        # Get GitHub data with error handling
        try:
            repositories = github_service.get_repositories(github_token)
            print(f"Found {len(repositories)} repositories")
        except Exception as e:
            print(f"Error getting repositories: {e}")
            repositories = []
        
        try:
            issues = github_service.get_issues(github_token)
            print(f"Found {len(issues)} issues")
        except Exception as e:
            print(f"Error getting issues: {e}")
            issues = []
        
        try:
            pull_requests = github_service.get_pull_requests(github_token)
            print(f"Found {len(pull_requests)} pull requests")
        except Exception as e:
            print(f"Error getting pull requests: {e}")
            pull_requests = []
        
        try:
            activity = github_service.get_activity(github_token)
            print(f"Found {len(activity)} activities")
        except Exception as e:
            print(f"Error getting activity: {e}")
            activity = []
        
        # Generate summary
        try:
            summary = github_ai_service.generate_github_summary(
                repositories, issues, pull_requests, activity
            )
        except Exception as e:
            print(f"Error generating summary: {e}")
            summary = f"Error generating summary: {str(e)}"
        
        # Count statistics
        repository_count = len(repositories)
        issue_count = len([i for i in issues if i.get('state') == 'open' and 'pull_request' not in i])
        pr_count = len(pull_requests)
        activity_count = len(activity)
        
        print(f"Statistics: {repository_count} repos, {issue_count} issues, {pr_count} PRs, {activity_count} activities")
        
        # Render dashboard template using utility function
        try:
            template = read_template_file("frontend/templates/github_dashboard.html")
            return HTMLResponse(safe_format(template,
                summary=summary,
                repository_count=repository_count,
                issue_count=issue_count,
                pr_count=pr_count,
                activity_count=activity_count
            ))
        except Exception as e:
            print(f"Error reading template: {e}")
            return HTMLResponse(f"""
                <html>
                <head><title>GitHub Dashboard</title></head>
                <body>
                    <h1>GitHub Dashboard</h1>
                    <p>Repositories: {repository_count}</p>
                    <p>Issues: {issue_count}</p>
                    <p>Pull Requests: {pr_count}</p>
                    <p>Activities: {activity_count}</p>
                    <h2>Summary:</h2>
                    <pre>{summary}</pre>
                </body>
                </html>
            """)
        
    except Exception as e:
        print(f"Error in github_dashboard: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error loading GitHub dashboard: {str(e)}")

@router.get("/summary")
async def get_github_summary(request: Request, user: Dict = Depends(get_current_user)):
    """Get GitHub summary"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        summary = github_service.get_github_summary(github_token)
        return summary
        
    except Exception as e:
        print(f"Error getting GitHub summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting GitHub summary: {str(e)}")

@router.get("/repositories")
async def get_repositories(request: Request, user: Dict = Depends(get_current_user)):
    """Get user repositories"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        repositories = github_service.get_repositories(github_token)
        return {"repositories": repositories}
        
    except Exception as e:
        print(f"Error getting repositories: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting repositories: {str(e)}")

@router.get("/issues")
async def get_issues(request: Request, user: Dict = Depends(get_current_user)):
    """Get user issues"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        issues = github_service.get_issues(github_token)
        return {"issues": issues}
        
    except Exception as e:
        print(f"Error getting issues: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting issues: {str(e)}")

@router.get("/pull-requests")
async def get_pull_requests(request: Request, user: Dict = Depends(get_current_user)):
    """Get user pull requests"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        pull_requests = github_service.get_pull_requests(github_token)
        return {"pull_requests": pull_requests}
        
    except Exception as e:
        print(f"Error getting pull requests: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting pull requests: {str(e)}")

@router.get("/activity")
async def get_activity(request: Request, user: Dict = Depends(get_current_user)):
    """Get user activity"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        activity = github_service.get_activity(github_token)
        return {"activity": activity}
        
    except Exception as e:
        print(f"Error getting activity: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting activity: {str(e)}")

@router.get("/chatbot/suggestions")
async def get_github_chatbot_suggestions():
    """Get GitHub chatbot suggestions"""
    try:
        suggestions = github_chatbot_service.get_suggestions()
        return {"suggestions": suggestions}
        
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")

@router.post("/chatbot/chat")
async def github_chatbot_chat(request: Request, user: Dict = Depends(get_current_user)):
    """Process GitHub chatbot message"""
    try:
        github_token = request.session.get('github_access_token')
        if not github_token:
            raise HTTPException(status_code=401, detail="GitHub not authenticated")
        
        # Get request body
        body = await request.json()
        message = body.get('message', '')
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get GitHub data for context
        repositories = github_service.get_repositories(github_token)
        issues = github_service.get_issues(github_token)
        pull_requests = github_service.get_pull_requests(github_token)
        activity = github_service.get_activity(github_token)
        
        github_data = {
            'repositories': repositories,
            'issues': issues,
            'pull_requests': pull_requests,
            'activity': activity
        }
        
        # Process message
        response = github_chatbot_service.process_message(message, github_data)
        
        return {"response": response}
        
    except Exception as e:
        print(f"Error processing chatbot message: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}") 