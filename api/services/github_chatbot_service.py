import google.generativeai as genai
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class GitHubChatbotService:
    """Service for GitHub chatbot functionality"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def chat_about_github(self, message: str, github_data: Dict) -> str:
        """Generate a response about GitHub data"""
        try:
            # Create context from GitHub data
            context = self._create_github_context(github_data)
            
            # Create the prompt
            prompt = f"""
You are a helpful GitHub assistant. You have access to the following GitHub data:

{context}

User Question: {message}

Please provide a helpful and informative response about the user's GitHub activity. 
Be specific and reference the actual data when possible. If the user asks about something 
not available in the data, politely explain what information is available.

Response:"""

            # Generate response
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error while processing your request: {str(e)}"
    
    def _create_github_context(self, github_data: Dict) -> str:
        """Create a context string from GitHub data"""
        context_parts = []
        
        # Repository information
        if github_data.get("repositories"):
            repos = github_data["repositories"]
            context_parts.append(f"Repositories ({len(repos)} total):")
            for repo in repos[:5]:  # Show first 5 repos
                context_parts.append(f"- {repo['full_name']}: {repo.get('description', 'No description')} ({repo['language'] or 'Unknown language'})")
            if len(repos) > 5:
                context_parts.append(f"... and {len(repos) - 5} more repositories")
        
        # Commit information
        if github_data.get("commits"):
            commits = github_data["commits"]
            context_parts.append(f"\nRecent Commits ({len(commits)} total):")
            for commit in commits[:5]:  # Show first 5 commits
                context_parts.append(f"- {commit['repository']}: {commit['commit']['message'][:100]}...")
            if len(commits) > 5:
                context_parts.append(f"... and {len(commits) - 5} more commits")
        
        # Issues information
        if github_data.get("issues"):
            issues = github_data["issues"]
            context_parts.append(f"\nIssues ({len(issues)} total):")
            for issue in issues[:5]:  # Show first 5 issues
                context_parts.append(f"- {issue['repository']}: {issue['title']} (State: {issue['state']})")
            if len(issues) > 5:
                context_parts.append(f"... and {len(issues) - 5} more issues")
        
        # Pull requests information
        if github_data.get("pull_requests"):
            prs = github_data["pull_requests"]
            context_parts.append(f"\nPull Requests ({len(prs)} total):")
            for pr in prs[:5]:  # Show first 5 PRs
                context_parts.append(f"- {pr['repository']}: {pr['title']} (State: {pr['state']})")
            if len(prs) > 5:
                context_parts.append(f"... and {len(prs) - 5} more pull requests")
        
        # Summary statistics
        context_parts.append(f"\nSummary Statistics:")
        context_parts.append(f"- Total Repositories: {github_data.get('total_repos', 0)}")
        context_parts.append(f"- Total Commits: {github_data.get('total_commits', 0)}")
        context_parts.append(f"- Total Issues: {github_data.get('total_issues', 0)}")
        context_parts.append(f"- Total Pull Requests: {github_data.get('total_pull_requests', 0)}")
        
        return "\n".join(context_parts)
    
    def get_github_suggestions(self) -> List[str]:
        """Get suggested questions for GitHub chatbot"""
        return [
            "How many repositories do I have?",
            "What are my most recent commits?",
            "Show me my open issues",
            "What languages do I use most?",
            "Which repositories are most active?",
            "How many pull requests do I have?",
            "What's my GitHub activity pattern?",
            "Which repositories have the most stars?"
        ] 