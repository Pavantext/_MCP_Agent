import google.generativeai as genai
from typing import List, Dict
from ..models.github import GitHubSummary
import os

class GitHubAIService:
    """AI service for GitHub data analysis and summarization"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def generate_github_summary(self, repositories: List[Dict], issues: List[Dict], 
                               pull_requests: List[Dict], activity: List[Dict]) -> str:
        """Generate AI-powered GitHub summary"""
        if not self.model:
            return self._generate_basic_summary(repositories, issues, pull_requests, activity)
        
        try:
            # Prepare data for AI analysis
            repo_data = []
            for repo in repositories[:10]:  # Top 10 repos
                repo_data.append({
                    'name': repo.get('name', 'Unknown'),
                    'language': repo.get('language', 'Unknown'),
                    'description': repo.get('description', 'No description'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'issues': repo.get('open_issues_count', 0)
                })
            
            issue_data = []
            for issue in issues[:10]:  # Top 10 issues
                issue_data.append({
                    'title': issue.get('title', 'No title'),
                    'state': issue.get('state', 'unknown'),
                    'repo': issue.get('repository', {}).get('name', 'Unknown'),
                    'created_at': issue.get('created_at', 'Unknown')
                })
            
            pr_data = []
            for pr in pull_requests[:10]:  # Top 10 PRs
                pr_data.append({
                    'title': pr.get('title', 'No title'),
                    'state': pr.get('state', 'unknown'),
                    'repo': pr.get('head', {}).get('repo', {}).get('name', 'Unknown'),
                    'created_at': pr.get('created_at', 'Unknown')
                })
            
            # Create prompt for AI
            prompt = f"""
            Analyze this GitHub data and provide a comprehensive, well-structured summary:
            
            Repositories ({len(repositories)} total):
            {repo_data}
            
            Issues ({len(issues)} total):
            {issue_data}
            
            Pull Requests ({len(pull_requests)} total):
            {pr_data}
            
            Recent Activity ({len(activity)} events):
            {activity[:10]}
            
            Please provide a detailed summary that includes:
            1. Overview of repositories (languages, top projects)
            2. Analysis of open issues and their priorities
            3. Review of pull requests and their status
            4. Recent activity patterns
            5. Recommendations for next actions
            
            Format the response with clear headings and bullet points.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating AI summary: {str(e)}")
            return self._generate_basic_summary(repositories, issues, pull_requests, activity)
    
    def _generate_basic_summary(self, repositories: List[Dict], issues: List[Dict], 
                               pull_requests: List[Dict], activity: List[Dict]) -> str:
        """Generate basic summary without AI"""
        summary_parts = []
        
        # Repository summary
        total_repos = len(repositories)
        languages = {}
        for repo in repositories:
            lang = repo.get('language', 'Unknown')
            languages[lang] = languages.get(lang, 0) + 1
        
        summary_parts.append(f"## Repository Overview")
        summary_parts.append(f"You have {total_repos} repositories with the following language distribution:")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
            summary_parts.append(f"- {lang}: {count} repositories")
        
        # Top repositories
        if repositories:
            summary_parts.append(f"\n## Top Repositories")
            for i, repo in enumerate(repositories[:5], 1):
                name = repo.get('name', 'Unknown')
                description = repo.get('description', 'No description')
                language = repo.get('language', 'Unknown')
                stars = repo.get('stargazers_count', 0)
                
                summary_parts.append(f"{i}. **{name}** ({language})")
                summary_parts.append(f"   {description}")
                summary_parts.append(f"   ⭐ {stars} stars")
                summary_parts.append("")
        
        # Issues summary
        if issues:
            summary_parts.append(f"## Open Issues ({len(issues)} total)")
            for i, issue in enumerate(issues[:5], 1):
                title = issue.get('title', 'No title')
                repo = issue.get('repository', {}).get('name', 'Unknown')
                state = issue.get('state', 'unknown')
                
                summary_parts.append(f"{i}. [{repo}] {title} ({state})")
            
            if len(issues) > 5:
                summary_parts.append(f"... and {len(issues) - 5} more issues")
        
        # Pull requests summary
        if pull_requests:
            summary_parts.append(f"\n## Open Pull Requests ({len(pull_requests)} total)")
            for i, pr in enumerate(pull_requests[:5], 1):
                title = pr.get('title', 'No title')
                repo = pr.get('head', {}).get('repo', {}).get('name', 'Unknown')
                state = pr.get('state', 'unknown')
                
                summary_parts.append(f"{i}. [{repo}] {title} ({state})")
            
            if len(pull_requests) > 5:
                summary_parts.append(f"... and {len(pull_requests) - 5} more pull requests")
        
        # Activity summary
        if activity:
            summary_parts.append(f"\n## Recent Activity")
            summary_parts.append(f"You have {len(activity)} recent activities including commits, issues, and pull requests.")
        
        return "\n".join(summary_parts)
    
    def analyze_github_patterns(self, repositories: List[Dict], issues: List[Dict], 
                               pull_requests: List[Dict]) -> Dict:
        """Analyze patterns in GitHub data"""
        analysis = {
            'top_languages': {},
            'most_active_repos': [],
            'issue_priorities': {},
            'pr_status_distribution': {},
            'recommendations': []
        }
        
        # Language analysis
        languages = {}
        for repo in repositories:
            lang = repo.get('language', 'Unknown')
            languages[lang] = languages.get(lang, 0) + 1
        
        analysis['top_languages'] = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Most active repositories
        sorted_repos = sorted(repositories, key=lambda x: x.get('updated_at', ''), reverse=True)
        analysis['most_active_repos'] = [repo.get('name') for repo in sorted_repos[:5]]
        
        # Issue analysis
        issue_states = {}
        for issue in issues:
            state = issue.get('state', 'unknown')
            issue_states[state] = issue_states.get(state, 0) + 1
        
        analysis['issue_priorities'] = issue_states
        
        # PR analysis
        pr_states = {}
        for pr in pull_requests:
            state = pr.get('state', 'unknown')
            pr_states[state] = pr_states.get(state, 0) + 1
        
        analysis['pr_status_distribution'] = pr_states
        
        # Generate recommendations
        if len(issues) > 10:
            analysis['recommendations'].append("Consider reviewing and closing old issues")
        
        if len(pull_requests) > 5:
            analysis['recommendations'].append("Review pending pull requests")
        
        if len(repositories) > 20:
            analysis['recommendations'].append("Consider archiving inactive repositories")
        
        return analysis 