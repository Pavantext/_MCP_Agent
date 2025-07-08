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

class GitHubRepository(BaseModel):
    """GitHub repository model"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    created_at: str
    updated_at: str
    private: bool
    html_url: str

class GitHubCommit(BaseModel):
    """GitHub commit model"""
    sha: str
    message: str
    author: Dict
    date: str
    repository: str

class GitHubIssue(BaseModel):
    """GitHub issue model"""
    id: int
    number: int
    title: str
    state: str
    user: Dict
    created_at: str
    updated_at: str
    repository: str

class GitHubPullRequest(BaseModel):
    """GitHub pull request model"""
    id: int
    number: int
    title: str
    state: str
    user: Dict
    created_at: str
    updated_at: str
    repository: str
    merged: bool 