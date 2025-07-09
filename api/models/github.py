from pydantic import BaseModel
from typing import List, Dict, Optional

class GitHubAuthStatus(BaseModel):
    """GitHub authentication status"""
    is_authenticated: bool
    message: str

class GitHubTokenResponse(BaseModel):
    """GitHub token response"""
    access_token: str

class GitHubError(BaseModel):
    """GitHub authentication error"""
    error: str
    error_description: str

class GitHubSummary(BaseModel):
    """GitHub summary response"""
    repositories: List[Dict]
    total_repos: int
    total_commits: int
    total_issues: int
    total_pull_requests: int
    summary: str 