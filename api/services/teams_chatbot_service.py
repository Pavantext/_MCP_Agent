import google.generativeai as genai
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class TeamsChatbotService:
    """Service for Teams chatbot functionality using AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def chat_about_teams(self, user_message: str, teams_data: Dict) -> str:
        """Generate a response about Teams data based on user query"""
        try:
            # Create a comprehensive prompt with Teams data
            prompt = self._create_teams_prompt(user_message, teams_data)
            
            # Generate response using AI
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while processing your request: {str(e)}"
    
    def _create_teams_prompt(self, user_message: str, teams_data: Dict) -> str:
        """Create a detailed prompt for Teams data analysis"""
        
        # Extract key information from teams_data
        teams = teams_data.get("teams", [])
        channels = teams_data.get("channels", [])
        messages = teams_data.get("messages", [])
        meetings = teams_data.get("meetings", [])
        total_teams = teams_data.get("total_teams", 0)
        total_channels = teams_data.get("total_channels", 0)
        total_messages = teams_data.get("total_messages", 0)
        total_chats = teams_data.get("total_chats", 0)
        total_meetings = teams_data.get("total_meetings", 0)
        
        # Create a summary of the data
        teams_summary = f"""
You have access to the following Microsoft Teams data:

**Teams Overview:**
- Total Teams: {total_teams}
- Total Channels: {total_channels}
- Total Messages: {total_messages}
- Total Personal Chats: {total_chats}
- Total Meetings: {total_meetings}

**Teams Details:**
"""
        
        for team in teams:
            teams_summary += f"- {team.get('displayName', 'Unknown Team')} (ID: {team.get('id', 'N/A')})\n"
        
        teams_summary += "\n**Channels by Team:**\n"
        team_channels = {}
        for channel in channels:
            team_name = channel.get("team_name", "Unknown Team")
            if team_name not in team_channels:
                team_channels[team_name] = []
            team_channels[team_name].append(channel.get("displayName", "Unknown Channel"))
        
        for team_name, channel_list in team_channels.items():
            teams_summary += f"- {team_name}: {', '.join(channel_list)}\n"
        
        # Add recent message activity
        teams_summary += "\n**Recent Message Activity:**\n"
        if messages:
            # Group messages by team/channel
            message_summary = {}
            for message in messages[:20]:  # Limit to recent messages
                source = message.get("team_name", "Personal Chat")
                if source not in message_summary:
                    message_summary[source] = 0
                message_summary[source] += 1
            
            for source, count in message_summary.items():
                teams_summary += f"- {source}: {count} recent messages\n"
        
        # Add meetings information
        if meetings:
            teams_summary += "\n**Recent Meetings:**\n"
            for meeting in meetings[:5]:  # Show recent 5 meetings
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
                
                teams_summary += f"- {meeting.get('subject', 'No Subject')} (Start: {formatted_time}, Organizer: {meeting.get('organizer', 'Unknown')})\n"
        
        prompt = f"""
You are a helpful Microsoft Teams assistant. You have access to the user's Teams data and can answer questions about their teams, channels, messages, meetings, and activity.

{teams_summary}

**User Question:** {user_message}

Please provide a helpful, informative response based on the Teams data above. Be conversational and helpful. If the user asks about specific information that's not available in the data, let them know what information is available instead.

Focus on:
- Team and channel information
- Message activity and patterns
- Recent communication trends
- Team collaboration insights
- Meeting schedules and patterns
- Online meeting participation

Keep your response concise but informative, and be helpful in guiding the user to understand their Teams usage.
"""
        
        return prompt
    
    def get_teams_insights(self, teams_data: Dict) -> Dict:
        """Generate insights about Teams usage"""
        try:
            teams = teams_data.get("teams", [])
            channels = teams_data.get("channels", [])
            messages = teams_data.get("messages", [])
            
            # Calculate insights
            total_teams = len(teams)
            total_channels = len(channels)
            total_messages = len(messages)
            
            # Most active teams (by message count)
            team_activity = {}
            for message in messages:
                team_name = message.get("team_name", "Personal Chat")
                if team_name not in team_activity:
                    team_activity[team_name] = 0
                team_activity[team_name] += 1
            
            most_active_teams = sorted(team_activity.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Most active channels
            channel_activity = {}
            for message in messages:
                if not message.get("is_personal_chat", False):
                    channel_name = message.get("channel_name", "Unknown")
                    team_name = message.get("team_name", "Unknown")
                    key = f"{team_name} - {channel_name}"
                    if key not in channel_activity:
                        channel_activity[key] = 0
                    channel_activity[key] += 1
            
            most_active_channels = sorted(channel_activity.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "total_teams": total_teams,
                "total_channels": total_channels,
                "total_messages": total_messages,
                "most_active_teams": most_active_teams,
                "most_active_channels": most_active_channels,
                "activity_level": "High" if total_messages > 100 else "Medium" if total_messages > 50 else "Low"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate insights: {str(e)}",
                "total_teams": 0,
                "total_channels": 0,
                "total_messages": 0
            } 