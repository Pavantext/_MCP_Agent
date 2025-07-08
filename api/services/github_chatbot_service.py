import google.generativeai as genai
from typing import List, Dict
import os

class GitHubChatbotService:
    """Chatbot service for GitHub-related queries"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def get_suggestions(self) -> List[str]:
        """Get suggested questions for GitHub chatbot"""
        return [
            "How many repositories do I have?",
            "Show me my open issues",
            "What are my most active repositories?",
            "How many pull requests are pending?",
            "What programming languages do I use most?",
            "Show me recent activity",
            "Which repositories need attention?",
            "How many stars do my repositories have?",
            "What are my top repositories by activity?",
            "Show me issues that need review"
        ]
    
    def process_message(self, message: str, github_data: Dict) -> str:
        """Process user message and return response"""
        if not self.model:
            return self._process_basic_message(message, github_data)
        
        try:
            # Prepare context from GitHub data
            context = self._prepare_context(github_data)
            
            prompt = f"""
            You are a helpful GitHub assistant. Use this GitHub data to answer the user's question:
            
            {context}
            
            User Question: {message}
            
            Provide a helpful, accurate response based on the GitHub data. If the information isn't available in the data, say so politely.
            Keep responses concise but informative.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return self._process_basic_message(message, github_data)
    
    def _prepare_context(self, github_data: Dict) -> str:
        """Prepare context string from GitHub data"""
        context_parts = []
        
        # Repository information
        repositories = github_data.get('repositories', [])
        if repositories:
            context_parts.append(f"Repositories: {len(repositories)} total")
            for repo in repositories[:5]:
                name = repo.get('name', 'Unknown')
                language = repo.get('language', 'Unknown')
                stars = repo.get('stargazers_count', 0)
                context_parts.append(f"- {name} ({language}, {stars} stars)")
        
        # Issues information
        issues = github_data.get('issues', [])
        if issues:
            open_issues = len([i for i in issues if i.get('state') == 'open'])
            context_parts.append(f"Issues: {len(issues)} total, {open_issues} open")
            for issue in issues[:3]:
                title = issue.get('title', 'No title')
                repo = issue.get('repository', {}).get('name', 'Unknown')
                context_parts.append(f"- [{repo}] {title}")
        
        # Pull requests information
        pull_requests = github_data.get('pull_requests', [])
        if pull_requests:
            open_prs = len([pr for pr in pull_requests if pr.get('state') == 'open'])
            context_parts.append(f"Pull Requests: {len(pull_requests)} total, {open_prs} open")
            for pr in pull_requests[:3]:
                title = pr.get('title', 'No title')
                repo = pr.get('head', {}).get('repo', {}).get('name', 'Unknown')
                context_parts.append(f"- [{repo}] {title}")
        
        # Activity information
        activity = github_data.get('activity', [])
        if activity:
            context_parts.append(f"Recent Activity: {len(activity)} events")
        
        return "\n".join(context_parts)
    
    def _process_basic_message(self, message: str, github_data: Dict) -> str:
        """Process message without AI"""
        message_lower = message.lower()
        
        repositories = github_data.get('repositories', [])
        issues = github_data.get('issues', [])
        pull_requests = github_data.get('pull_requests', [])
        activity = github_data.get('activity', [])
        
        # Repository queries
        if any(word in message_lower for word in ['repository', 'repo', 'repositories']):
            total_repos = len(repositories)
            languages = {}
            for repo in repositories:
                lang = repo.get('language', 'Unknown')
                languages[lang] = languages.get(lang, 0) + 1
            
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
            lang_str = ", ".join([f"{lang} ({count})" for lang, count in top_languages])
            
            return f"You have {total_repos} repositories. Top languages: {lang_str}"
        
        # Issue queries
        elif any(word in message_lower for word in ['issue', 'issues']):
            open_issues = len([i for i in issues if i.get('state') == 'open'])
            total_issues = len(issues)
            
            if 'open' in message_lower:
                return f"You have {open_issues} open issues out of {total_issues} total issues."
            else:
                return f"You have {total_issues} issues, with {open_issues} currently open."
        
        # Pull request queries
        elif any(word in message_lower for word in ['pull request', 'pr', 'pull']):
            open_prs = len([pr for pr in pull_requests if pr.get('state') == 'open'])
            total_prs = len(pull_requests)
            
            if 'pending' in message_lower or 'open' in message_lower:
                return f"You have {open_prs} open pull requests out of {total_prs} total."
            else:
                return f"You have {total_prs} pull requests, with {open_prs} currently open."
        
        # Activity queries
        elif any(word in message_lower for word in ['activity', 'recent', 'latest']):
            return f"You have {len(activity)} recent activities including commits, issues, and pull requests."
        
        # Language queries
        elif any(word in message_lower for word in ['language', 'languages', 'programming']):
            languages = {}
            for repo in repositories:
                lang = repo.get('language', 'Unknown')
                languages[lang] = languages.get(lang, 0) + 1
            
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            lang_list = [f"{lang} ({count} repos)" for lang, count in top_languages]
            
            return f"Your top programming languages: {', '.join(lang_list)}"
        
        # Star queries
        elif 'star' in message_lower:
            total_stars = sum(repo.get('stargazers_count', 0) for repo in repositories)
            return f"Your repositories have a total of {total_stars} stars."
        
        # Default response
        else:
            return "I can help you with information about your repositories, issues, pull requests, and activity. Try asking about specific aspects of your GitHub account." 