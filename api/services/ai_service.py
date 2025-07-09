import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Constants
GEMINI_MODEL_NAME = 'gemini-1.5-flash'
MAX_EMAILS_FOR_AI_PROCESSING = 30
MAX_EMAILS_FOR_FALLBACK = 15
MAX_REPOS_FOR_AI = 10
MAX_ITEMS_FOR_AI = 10

class AIService:
    """Service for AI-powered email and GitHub summarization"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    
    def summarize_emails(self, emails: List[Dict]) -> str:
        """Generate AI summary of emails"""
        if not emails:
            return "No emails to summarize."
        
        # Count unread emails
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        # Prepare email data for AI
        email_texts = []
        for email in emails[:MAX_EMAILS_FOR_AI_PROCESSING]:
            email_text = self._format_email_for_ai(email)
            email_texts.append(email_text)
        
        # Create prompt for AI
        prompt = self._create_email_summary_prompt(email_texts, total_count, unread_count)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI summary: {str(e)}")
            return self._fallback_summary(emails)
    
    def _format_email_for_ai(self, email: Dict) -> str:
        """Format email data for AI processing"""
        from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
        subject = email.get("subject", "No Subject")
        body_preview = email.get("bodyPreview", "")
        received = email.get("receivedDateTime", "Unknown")
        is_read = email.get("isRead", True)
        status = "UNREAD" if not is_read else "READ"
        
        return f"""
Status: {status}
From: {from_info}
Subject: {subject}
Received: {received}
Preview: {body_preview}
---
"""
    
    def _create_email_summary_prompt(self, email_texts: List[str], total_count: int, unread_count: int) -> str:
        """Create prompt for email summary"""
        return f"""
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
    
    def _fallback_summary(self, emails: List[Dict]) -> str:
        """Fallback summary when AI fails"""
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        html_parts = []
        html_parts.append(f'<h2>📧 Email Summary</h2>')
        html_parts.append(f'<p><strong>Total Emails:</strong> {total_count} | <strong>Unread:</strong> {unread_count}</p>')
        html_parts.append('<h3>Recent Emails:</h3>')
        html_parts.append('<ul>')
        
        for i, email in enumerate(emails[:MAX_EMAILS_FOR_FALLBACK], 1):
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            is_read = email.get("isRead", True)
            status = "📬" if not is_read else "📭"
            
            html_parts.append(f'<li><strong>{status} {from_info}:</strong> {subject}</li>')
        
        html_parts.append('</ul>')
        
        if len(emails) > MAX_EMAILS_FOR_FALLBACK:
            html_parts.append(f'<p><em>... and {len(emails) - MAX_EMAILS_FOR_FALLBACK} more emails</em></p>')
        
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
        context_parts = self._create_github_context_for_ai(repos, commits, issues, pull_requests)
        
        # Create prompt for AI
        prompt = self._create_github_summary_prompt(context_parts, repos, commits, issues, pull_requests)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating GitHub AI summary: {str(e)}")
            return self._fallback_github_summary(github_data)
    
    def _create_github_context_for_ai(self, repos: List[Dict], commits: List[Dict], issues: List[Dict], pull_requests: List[Dict]) -> List[str]:
        """Create context from GitHub data for AI processing"""
        context_parts = []
        
        # Repository information
        if repos:
            context_parts.append(f"Repositories ({len(repos)} total):")
            for repo in repos[:MAX_REPOS_FOR_AI]:
                context_parts.append(f"- {repo['full_name']}: {repo.get('description', 'No description')} ({repo['language'] or 'Unknown'}) - Stars: {repo['stargazers_count']}, Forks: {repo['forks_count']}")
        
        # Commit information
        if commits:
            context_parts.append(f"\nRecent Commits ({len(commits)} total):")
            for commit in commits[:MAX_ITEMS_FOR_AI]:
                context_parts.append(f"- {commit['repository']}: {commit['commit']['message'][:100]}...")
        
        # Issues information
        if issues:
            context_parts.append(f"\nIssues ({len(issues)} total):")
            for issue in issues[:MAX_ITEMS_FOR_AI]:
                context_parts.append(f"- {issue['repository']}: {issue['title']} (State: {issue['state']})")
        
        # Pull requests information
        if pull_requests:
            context_parts.append(f"\nPull Requests ({len(pull_requests)} total):")
            for pr in pull_requests[:MAX_ITEMS_FOR_AI]:
                context_parts.append(f"- {pr['repository']}: {pr['title']} (State: {pr['state']})")
        
        return context_parts
    
    def _create_github_summary_prompt(self, context_parts: List[str], repos: List[Dict], commits: List[Dict], issues: List[Dict], pull_requests: List[Dict]) -> str:
        """Create prompt for GitHub summary"""
        return f"""
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
            for repo in repos[:MAX_REPOS_FOR_AI]:
                html_parts.append(f'<li><strong>📦 {repo["full_name"]}:</strong> {repo.get("description", "No description")} ({repo["language"] or "Unknown"}) - ⭐ {repo["stargazers_count"]} stars</li>')
            html_parts.append('</ul>')
        
        if commits:
            html_parts.append('<h3>Recent Commits:</h3>')
            html_parts.append('<ul>')
            for commit in commits[:MAX_ITEMS_FOR_AI]:
                html_parts.append(f'<li><strong>💻 {commit["repository"]}:</strong> {commit["commit"]["message"][:100]}...</li>')
            html_parts.append('</ul>')
        
        if issues:
            html_parts.append('<h3>Recent Issues:</h3>')
            html_parts.append('<ul>')
            for issue in issues[:MAX_ITEMS_FOR_AI]:
                status = "🔴" if issue["state"] == "open" else "🟢"
                html_parts.append(f'<li><strong>{status} {issue["repository"]}:</strong> {issue["title"]}</li>')
            html_parts.append('</ul>')
        
        return "".join(html_parts)
    
    def summarize_teams_data(self, teams_data: Dict) -> str:
        """Generate AI summary of Teams data"""
        if not teams_data:
            return "No Teams data to summarize."
        
        # Prepare Teams data for AI
        teams = teams_data.get("teams", [])
        channels = teams_data.get("channels", [])
        messages = teams_data.get("messages", [])
        meetings = teams_data.get("meetings", [])
        
        # Create detailed context for AI
        context_parts = self._create_teams_context_for_ai(teams, channels, messages, meetings)
        
        # Create prompt for AI
        prompt = self._create_teams_summary_prompt(context_parts, teams, channels, messages, meetings)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating Teams AI summary: {str(e)}")
            return self._fallback_teams_summary(teams_data)
    
    def _create_teams_context_for_ai(self, teams: List[Dict], channels: List[Dict], messages: List[Dict], meetings: List[Dict] = None) -> List[str]:
        """Create context from Teams data for AI processing"""
        context_parts = []
        
        # Teams information
        if teams:
            context_parts.append(f"Teams ({len(teams)} total):")
            for team in teams[:MAX_ITEMS_FOR_AI]:
                context_parts.append(f"- {team.get('displayName', 'Unknown Team')} (ID: {team.get('id', 'N/A')})")
        
        # Channels information
        if channels:
            context_parts.append(f"\nChannels ({len(channels)} total):")
            team_channels = {}
            for channel in channels:
                team_name = channel.get("team_name", "Unknown Team")
                if team_name not in team_channels:
                    team_channels[team_name] = []
                team_channels[team_name].append(channel.get("displayName", "Unknown Channel"))
            
            for team_name, channel_list in team_channels.items():
                context_parts.append(f"- {team_name}: {', '.join(channel_list[:5])}")
        
        # Messages information
        if messages:
            context_parts.append(f"\nRecent Messages ({len(messages)} total):")
            message_summary = {}
            for message in messages[:MAX_ITEMS_FOR_AI]:
                source = message.get("team_name", "Personal Chat")
                if source not in message_summary:
                    message_summary[source] = 0
                message_summary[source] += 1
            
            for source, count in message_summary.items():
                context_parts.append(f"- {source}: {count} messages")
        
        # Meetings information
        if meetings:
            context_parts.append(f"\nMeetings ({len(meetings)} total):")
            for meeting in meetings[:MAX_ITEMS_FOR_AI]:
                start_time = meeting.get("start", "Unknown")
                if start_time and "T" in start_time:
                    # Format the date for better readability
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_time = start_time
                else:
                    formatted_time = start_time
                
                context_parts.append(f"- {meeting.get('subject', 'No Subject')} (Start: {formatted_time}, Organizer: {meeting.get('organizer', 'Unknown')})")
        
        return context_parts
    
    def _create_teams_summary_prompt(self, context_parts: List[str], teams: List[Dict], channels: List[Dict], messages: List[Dict], meetings: List[Dict] = None) -> str:
        """Create prompt for Teams summary"""
        meetings_count = len(meetings) if meetings else 0
        
        return f"""
You are an AI assistant that summarizes Microsoft Teams activity. Please provide a comprehensive, well-organized summary of the following Teams data:

{''.join(context_parts)}

Summary Statistics:
- Total Teams: {len(teams)}
- Total Channels: {len(channels)}
- Total Messages: {len(messages)}
- Total Meetings: {meetings_count}

Focus on:
1. Team collaboration patterns and activity levels
2. Most active teams and channels
3. Communication trends and patterns
4. Personal vs team communication balance
5. Recent conversation topics and themes
6. Team structure and organization
7. Meeting patterns and scheduling
8. Online meeting participation

Please provide a clear, structured summary using HTML formatting. Use:
- <h2> for main sections
- <h3> for subsections
- <strong> for emphasis
- <ul> and <li> for lists
- <p> for paragraphs

Format the response as clean HTML that will display nicely in a web browser.
"""
    
    def _fallback_teams_summary(self, teams_data: Dict) -> str:
        """Fallback summary when AI fails for Teams data"""
        teams = teams_data.get("teams", [])
        channels = teams_data.get("channels", [])
        messages = teams_data.get("messages", [])
        meetings = teams_data.get("meetings", [])
        
        html_parts = []
        html_parts.append(f'<h2>💬 Teams Summary</h2>')
        html_parts.append(f'<p><strong>Total Teams:</strong> {len(teams)} | <strong>Channels:</strong> {len(channels)} | <strong>Messages:</strong> {len(messages)} | <strong>Meetings:</strong> {len(meetings)}</p>')
        
        if teams:
            html_parts.append('<h3>Your Teams:</h3>')
            html_parts.append('<ul>')
            for team in teams[:MAX_ITEMS_FOR_AI]:
                html_parts.append(f'<li><strong>👥 {team.get("displayName", "Unknown Team")}</strong></li>')
            html_parts.append('</ul>')
        
        if channels:
            html_parts.append('<h3>Active Channels:</h3>')
            html_parts.append('<ul>')
            team_channels = {}
            for channel in channels:
                team_name = channel.get("team_name", "Unknown Team")
                if team_name not in team_channels:
                    team_channels[team_name] = []
                team_channels[team_name].append(channel.get("displayName", "Unknown Channel"))
            
            for team_name, channel_list in team_channels.items():
                html_parts.append(f'<li><strong>📢 {team_name}:</strong> {", ".join(channel_list[:3])}</li>')
            html_parts.append('</ul>')
        
        if messages:
            html_parts.append('<h3>Recent Activity:</h3>')
            html_parts.append('<ul>')
            message_summary = {}
            for message in messages[:MAX_ITEMS_FOR_AI]:
                source = message.get("team_name", "Personal Chat")
                if source not in message_summary:
                    message_summary[source] = 0
                message_summary[source] += 1
            
            for source, count in message_summary.items():
                html_parts.append(f'<li><strong>💬 {source}:</strong> {count} recent messages</li>')
            html_parts.append('</ul>')
        
        if meetings:
            html_parts.append('<h3>Upcoming Meetings:</h3>')
            html_parts.append('<ul>')
            for meeting in meetings[:MAX_ITEMS_FOR_AI]:
                start_time = meeting.get("start", "Unknown")
                if start_time and "T" in start_time:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_time = start_time
                else:
                    formatted_time = start_time
                
                html_parts.append(f'<li><strong>📅 {meeting.get("subject", "No Subject")}</strong> - {formatted_time} (Organizer: {meeting.get("organizer", "Unknown")})</li>')
            html_parts.append('</ul>')
        
        return "".join(html_parts) 