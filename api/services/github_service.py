import requests
from typing import List, Dict, Optional
from ..models.github import GitHubSummary, Repository, Issue, PullRequest, Activity

class GitHubService:
    """Service for handling GitHub API operations"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
    
    def get_user_info(self, access_token: str) -> Dict:
        """Get authenticated user information"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(f"{self.base_url}/user", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user info: {str(e)}")
            return {}
    
    def get_repositories(self, access_token: str) -> List[Dict]:
        """Get user's repositories"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(f"{self.base_url}/user/repos?sort=updated&per_page=50", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {str(e)}")
            return []
    
    def get_issues(self, access_token: str) -> List[Dict]:
        """Get user's issues (assigned and created)"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        issues = []
        
        try:
            # Get assigned issues
            response = requests.get(f"{self.base_url}/issues?filter=assigned&state=open&per_page=30", headers=headers)
            response.raise_for_status()
            issues.extend(response.json())
            
            # Get created issues
            response = requests.get(f"{self.base_url}/issues?filter=created&state=open&per_page=30", headers=headers)
            response.raise_for_status()
            issues.extend(response.json())
            
            return issues
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues: {str(e)}")
            return []
    
    def get_pull_requests(self, access_token: str) -> List[Dict]:
        """Get user's pull requests"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Get pull requests from issues endpoint with type=pr filter
            response = requests.get(f"{self.base_url}/issues?filter=assigned&state=open&per_page=30", headers=headers)
            response.raise_for_status()
            all_issues = response.json()
            
            # Filter for pull requests (issues with pull_request field)
            pull_requests = [issue for issue in all_issues if 'pull_request' in issue]
            
            return pull_requests
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pull requests: {str(e)}")
            return []
    
    def get_activity(self, access_token: str) -> List[Dict]:
        """Get user's recent activity"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            user_info = self.get_user_info(access_token)
            username = user_info.get('login', '')
            if not username:
                return []
            
            response = requests.get(f"{self.base_url}/users/{username}/events?per_page=30", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching activity: {str(e)}")
            return []
    
    def get_github_summary(self, access_token: str) -> GitHubSummary:
        """Get comprehensive GitHub summary"""
        try:
            user_info = self.get_user_info(access_token)
            repositories = self.get_repositories(access_token)
            issues = self.get_issues(access_token)
            pull_requests = self.get_pull_requests(access_token)
            activity = self.get_activity(access_token)
            
            # Count statistics
            total_repos = len(repositories)
            open_issues = len([i for i in issues if i.get('state') == 'open' and 'pull_request' not in i])
            open_prs = len(pull_requests)
            recent_activity = len(activity)
            
            # Create summary
            summary_parts = []
            summary_parts.append(f"Found {total_repos} repositories, {open_issues} open issues, {open_prs} open pull requests")
            
            # Top repositories
            if repositories:
                summary_parts.append("\nTop Repositories:")
                for i, repo in enumerate(repositories[:5], 1):
                    name = repo.get('name', 'Unknown')
                    description = repo.get('description', 'No description')
                    language = repo.get('language', 'Unknown')
                    stars = repo.get('stargazers_count', 0)
                    
                    summary_parts.append(f"{i}. {name} ({language})")
                    summary_parts.append(f"   Description: {description}")
                    summary_parts.append(f"   Stars: {stars}")
                    summary_parts.append("")
            
            # Recent issues
            if issues:
                summary_parts.append("Recent Issues:")
                for i, issue in enumerate(issues[:5], 1):
                    title = issue.get('title', 'No title')
                    repo = issue.get('repository', {}).get('name', 'Unknown')
                    state = issue.get('state', 'unknown')
                    
                    summary_parts.append(f"{i}. [{repo}] {title} ({state})")
                
                if len(issues) > 5:
                    summary_parts.append(f"... and {len(issues) - 5} more issues")
            
            return GitHubSummary(
                summary="\n".join(summary_parts),
                repository_count=total_repos,
                issue_count=open_issues,
                pull_request_count=open_prs,
                activity_count=recent_activity
            )
            
        except Exception as e:
            return GitHubSummary(
                summary=f"Error fetching GitHub data: {str(e)}",
                repository_count=0,
                issue_count=0,
                pull_request_count=0,
                activity_count=0
            ) 