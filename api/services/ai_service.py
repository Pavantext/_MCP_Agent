import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """Service for AI-powered email and GitHub summarization"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def summarize_emails(self, emails: List[Dict]) -> str:
        """Generate AI summary of emails"""
        if not emails:
            return "No emails to summarize."
        
        # Count unread emails
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        # Prepare email data for AI
        email_texts = []
        for email in emails[:30]:  # Limit to 30 emails for AI processing
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            body_preview = email.get("bodyPreview", "")
            received = email.get("receivedDateTime", "Unknown")
            is_read = email.get("isRead", True)
            status = "UNREAD" if not is_read else "READ"
            
            email_text = f"""
Status: {status}
From: {from_info}
Subject: {subject}
Received: {received}
Preview: {body_preview}
---
"""
            email_texts.append(email_text)
        
        # Create prompt for AI
        prompt = f"""
You are an AI assistant that summarizes emails. Please provide a comprehensive, well-organized summary of the following {len(email_texts)} emails (out of {total_count} total emails, with {unread_count} unread).

Focus on:
1. Key themes and topics across all emails
2. Important senders and their frequency
3. Urgent or time-sensitive items (especially unread ones)
4. Email patterns and trends
5. Unread vs read email distribution
6. Action items or follow-ups needed

Here are the emails:

{''.join(email_texts)}

Please provide a clear, structured summary using HTML formatting. Use:
- <h2> for main sections
- <h3> for subsections
- <strong> for emphasis
- <ul> and <li> for lists
- <p> for paragraphs

Format the response as clean HTML that will display nicely in a web browser.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI summary: {str(e)}")
            return self._fallback_summary(emails)
    
    def _fallback_summary(self, emails: List[Dict]) -> str:
        """Fallback summary when AI fails"""
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        html_parts = []
        html_parts.append(f'<h2>📧 Email Summary</h2>')
        html_parts.append(f'<p><strong>Total Emails:</strong> {total_count} | <strong>Unread:</strong> {unread_count}</p>')
        html_parts.append('<h3>Recent Emails:</h3>')
        html_parts.append('<ul>')
        
        for i, email in enumerate(emails[:15], 1):
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            is_read = email.get("isRead", True)
            status = "📬" if not is_read else "📭"
            
            html_parts.append(f'<li><strong>{status} {from_info}:</strong> {subject}</li>')
        
        html_parts.append('</ul>')
        
        if len(emails) > 15:
            html_parts.append(f'<p><em>... and {len(emails) - 15} more emails</em></p>')
        
        return "".join(html_parts)
    
    def summarize_github_data(self, github_data: Dict) -> str:
        """Generate AI summary of GitHub data"""
        if not github_data:
            return "No GitHub data to summarize."
        
        # Prepare GitHub data for AI
        repos = github_data.get("repositories", [])
        commits = github_data.get("commits", [])
        issues = github_data.get("issues", [])
        pull_requests = github_data.get("pull_requests", [])
        
        # Create detailed context for AI
        context_parts = []
        
        # Repository information
        if repos:
            context_parts.append(f"Repositories ({len(repos)} total):")
            for repo in repos[:10]:  # Show first 10 repos
                context_parts.append(f"- {repo['full_name']}: {repo.get('description', 'No description')} ({repo['language'] or 'Unknown'}) - Stars: {repo['stargazers_count']}, Forks: {repo['forks_count']}")
        
        # Commit information
        if commits:
            context_parts.append(f"\nRecent Commits ({len(commits)} total):")
            for commit in commits[:10]:  # Show first 10 commits
                context_parts.append(f"- {commit['repository']}: {commit['commit']['message'][:100]}...")
        
        # Issues information
        if issues:
            context_parts.append(f"\nIssues ({len(issues)} total):")
            for issue in issues[:10]:  # Show first 10 issues
                context_parts.append(f"- {issue['repository']}: {issue['title']} (State: {issue['state']})")
        
        # Pull requests information
        if pull_requests:
            context_parts.append(f"\nPull Requests ({len(pull_requests)} total):")
            for pr in pull_requests[:10]:  # Show first 10 PRs
                context_parts.append(f"- {pr['repository']}: {pr['title']} (State: {pr['state']})")
        
        # Create prompt for AI
        prompt = f"""
You are an AI assistant that summarizes GitHub activity. Please provide a comprehensive, well-organized summary of the following GitHub data:

{''.join(context_parts)}

Summary Statistics:
- Total Repositories: {len(repos)}
- Total Commits: {len(commits)}
- Total Issues: {len(issues)}
- Total Pull Requests: {len(pull_requests)}

Focus on:
1. Most active repositories and their purposes
2. Recent development activity and patterns
3. Programming languages used
4. Collaboration patterns (issues, PRs)
5. Repository popularity (stars, forks)
6. Development trends and insights

Please provide a clear, structured summary using HTML formatting. Use:
- <h2> for main sections
- <h3> for subsections
- <strong> for emphasis
- <ul> and <li> for lists
- <p> for paragraphs

Format the response as clean HTML that will display nicely in a web browser.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating GitHub AI summary: {str(e)}")
            return self._fallback_github_summary(github_data)
    
    def _fallback_github_summary(self, github_data: Dict) -> str:
        """Fallback summary when AI fails for GitHub data"""
        repos = github_data.get("repositories", [])
        commits = github_data.get("commits", [])
        issues = github_data.get("issues", [])
        pull_requests = github_data.get("pull_requests", [])
        
        html_parts = []
        html_parts.append(f'<h2>🐙 GitHub Summary</h2>')
        html_parts.append(f'<p><strong>Total Repositories:</strong> {len(repos)} | <strong>Commits:</strong> {len(commits)} | <strong>Issues:</strong> {len(issues)} | <strong>Pull Requests:</strong> {len(pull_requests)}</p>')
        
        if repos:
            html_parts.append('<h3>Top Repositories:</h3>')
            html_parts.append('<ul>')
            for repo in repos[:10]:
                html_parts.append(f'<li><strong>📦 {repo["full_name"]}:</strong> {repo.get("description", "No description")} ({repo["language"] or "Unknown"}) - ⭐ {repo["stargazers_count"]} stars</li>')
            html_parts.append('</ul>')
        
        if commits:
            html_parts.append('<h3>Recent Commits:</h3>')
            html_parts.append('<ul>')
            for commit in commits[:10]:
                html_parts.append(f'<li><strong>💻 {commit["repository"]}:</strong> {commit["commit"]["message"][:100]}...</li>')
            html_parts.append('</ul>')
        
        if issues:
            html_parts.append('<h3>Recent Issues:</h3>')
            html_parts.append('<ul>')
            for issue in issues[:10]:
                status = "🔴" if issue["state"] == "open" else "🟢"
                html_parts.append(f'<li><strong>{status} {issue["repository"]}:</strong> {issue["title"]}</li>')
            html_parts.append('</ul>')
        
        return "".join(html_parts) 