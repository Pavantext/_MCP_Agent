import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class GitHubService:
    """Service for fetching GitHub data"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
    
    def _get_headers(self, token: str) -> Dict:
        """Get headers with authentication token"""
        headers = self.headers.copy()
        headers["Authorization"] = f"token {token}"
        return headers
    
    def get_user_repositories(self, token: str, per_page: int = 100) -> List[Dict]:
        """Get user's repositories"""
        try:
            headers = self._get_headers(token)
            url = f"{self.base_url}/user/repos"
            params = {
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get repositories: {str(e)}")
    
    def get_repository_commits(self, token: str, repo_name: str, since_days: int = 30) -> List[Dict]:
        """Get commits for a specific repository"""
        try:
            headers = self._get_headers(token)
            url = f"{self.base_url}/repos/{repo_name}/commits"
            
            # Get commits from the last N days
            since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
            params = {
                "since": since_date,
                "per_page": 100
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            commits = response.json()
            
            # Add repository name to each commit
            for commit in commits:
                commit["repository"] = repo_name
            
            return commits
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get commits for {repo_name}: {str(e)}")
    
    def get_user_issues(self, token: str, state: str = "all") -> List[Dict]:
        """Get user's issues"""
        try:
            headers = self._get_headers(token)
            url = f"{self.base_url}/issues"
            params = {
                "filter": "all",
                "state": state,
                "per_page": 100,
                "sort": "updated",
                "direction": "desc"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            issues = response.json()
            
            # Add repository name to each issue
            for issue in issues:
                if "repository" in issue:
                    issue["repository"] = issue["repository"]["full_name"]
                else:
                    issue["repository"] = "Unknown"
            
            return issues
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get issues: {str(e)}")
    
    def get_user_pull_requests(self, token: str, state: str = "all") -> List[Dict]:
        """Get user's pull requests"""
        try:
            headers = self._get_headers(token)
            url = f"{self.base_url}/search/issues"
            query = f"author:{self._get_username(token)} is:pr"
            if state != "all":
                query += f" state:{state}"
            
            params = {
                "q": query,
                "per_page": 100,
                "sort": "updated",
                "order": "desc"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            pull_requests = data.get("items", [])
            
            # Add repository name to each PR
            for pr in pull_requests:
                if "repository" in pr:
                    pr["repository"] = pr["repository"]["full_name"]
                else:
                    pr["repository"] = "Unknown"
            
            return pull_requests
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get pull requests: {str(e)}")
    
    def _get_username(self, token: str) -> str:
        """Get GitHub username from token"""
        try:
            headers = self._get_headers(token)
            response = requests.get(f"{self.base_url}/user", headers=headers)
            response.raise_for_status()
            return response.json()["login"]
        except:
            return "unknown"
    
    def get_all_github_data(self, token: str) -> Dict:
        """Get all GitHub data for the user"""
        try:
            # Get repositories
            repositories = self.get_user_repositories(token)
            
            # Get commits for each repository
            all_commits = []
            for repo in repositories[:10]:  # Limit to first 10 repos to avoid rate limits
                try:
                    commits = self.get_repository_commits(token, repo["full_name"])
                    all_commits.extend(commits)
                except Exception as e:
                    print(f"Warning: Could not get commits for {repo['full_name']}: {e}")
            
            # Get issues
            issues = self.get_user_issues(token)
            
            # Get pull requests
            pull_requests = self.get_user_pull_requests(token)
            
            return {
                "repositories": repositories,
                "commits": all_commits,
                "issues": issues,
                "pull_requests": pull_requests,
                "total_repos": len(repositories),
                "total_commits": len(all_commits),
                "total_issues": len(issues),
                "total_pull_requests": len(pull_requests)
            }
        except Exception as e:
            raise Exception(f"Failed to get GitHub data: {str(e)}")
    
    def get_github_summary(self, token: str) -> Dict:
        """Get a summary of GitHub activity"""
        try:
            data = self.get_all_github_data(token)
            
            # Create a summary text
            summary_parts = []
            
            if data["total_repos"] > 0:
                summary_parts.append(f"You have {data['total_repos']} repositories")
            
            if data["total_commits"] > 0:
                summary_parts.append(f"with {data['total_commits']} recent commits")
            
            if data["total_issues"] > 0:
                summary_parts.append(f"{data['total_issues']} issues")
            
            if data["total_pull_requests"] > 0:
                summary_parts.append(f"{data['total_pull_requests']} pull requests")
            
            summary = " and ".join(summary_parts) + "."
            
            return {
                **data,
                "summary": summary
            }
        except Exception as e:
            raise Exception(f"Failed to get GitHub summary: {str(e)}") 