from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Repository(BaseModel):
    """GitHub repository model"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    updated_at: datetime
    html_url: str
    private: bool

class Issue(BaseModel):
    """GitHub issue model"""
    id: int
    number: int
    title: str
    body: Optional[str]
    state: str
    created_at: datetime
    updated_at: datetime
    repository: Repository
    user: dict
    assignees: List[dict]
    labels: List[dict]

class PullRequest(BaseModel):
    """GitHub pull request model"""
    id: int
    number: int
    title: str
    body: Optional[str]
    state: str
    created_at: datetime
    updated_at: datetime
    repository: Repository
    user: dict
    assignees: List[dict]
    labels: List[dict]
    head: dict
    base: dict

class Activity(BaseModel):
    """GitHub activity model"""
    id: str
    type: str
    actor: dict
    repo: dict
    payload: dict
    created_at: datetime

class GitHubSummary(BaseModel):
    """GitHub summary model"""
    summary: str
    repository_count: int
    issue_count: int
    pull_request_count: int
    activity_count: int 