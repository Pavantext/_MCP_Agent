import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..models.teams import TeamsSummary

class TeamsService:
    """Service for interacting with Microsoft Teams via Graph API"""
    
    def __init__(self):
        self.base_url = "https://graph.microsoft.com/v1.0"
    
    def get_user_teams(self, access_token: str) -> List[Dict]:
        """Get user's teams"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.base_url}/me/joinedTeams", headers=headers)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting teams: {e}")
            return []
    
    def get_team_channels(self, access_token: str, team_id: str) -> List[Dict]:
        """Get channels for a specific team"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.base_url}/teams/{team_id}/channels", headers=headers)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting channels for team {team_id}: {e}")
            return []
    
    def get_channel_messages(self, access_token: str, team_id: str, channel_id: str, limit: int = 50) -> List[Dict]:
        """Get messages from a specific channel"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Try without date filter first (some channels don't support it)
            try:
                response = requests.get(
                    f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages",
                    headers=headers,
                    params={
                        "$top": limit,
                        "$orderby": "createdDateTime desc"
                    }
                )
                response.raise_for_status()
                return response.json().get("value", [])
            except requests.exceptions.RequestException as e:
                if "400" in str(e):
                    # If 400 error, try with date filter but handle gracefully
                    since_date = (datetime.now() - timedelta(days=7)).isoformat() + "Z"
                    try:
                        response = requests.get(
                            f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages",
                            headers=headers,
                            params={
                                "$top": limit,
                                "$filter": f"createdDateTime ge {since_date}",
                                "$orderby": "createdDateTime desc"
                            }
                        )
                        response.raise_for_status()
                        return response.json().get("value", [])
                    except requests.exceptions.RequestException as e2:
                        print(f"Error getting messages for channel {channel_id} (with filter): {e2}")
                        return []
                else:
                    print(f"Error getting messages for channel {channel_id}: {e}")
                    return []
        except Exception as e:
            print(f"Unexpected error getting messages for channel {channel_id}: {e}")
            return []
    
    def get_chats(self, access_token: str) -> List[Dict]:
        """Get user's chats"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.base_url}/me/chats", headers=headers)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting chats: {e}")
            return []
    
    def get_chat_messages(self, access_token: str, chat_id: str, limit: int = 50) -> List[Dict]:
        """Get messages from a specific chat"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Try without date filter first (some chat types don't support it)
            try:
                response = requests.get(
                    f"{self.base_url}/chats/{chat_id}/messages",
                    headers=headers,
                    params={
                        "$top": limit,
                        "$orderby": "createdDateTime desc"
                    }
                )
                response.raise_for_status()
                return response.json().get("value", [])
            except requests.exceptions.RequestException as e:
                if "400" in str(e):
                    # If 400 error, try with date filter but handle gracefully
                    since_date = (datetime.now() - timedelta(days=7)).isoformat() + "Z"
                    try:
                        response = requests.get(
                            f"{self.base_url}/chats/{chat_id}/messages",
                            headers=headers,
                            params={
                                "$top": limit,
                                "$filter": f"createdDateTime ge {since_date}",
                                "$orderby": "createdDateTime desc"
                            }
                        )
                        response.raise_for_status()
                        return response.json().get("value", [])
                    except requests.exceptions.RequestException as e2:
                        print(f"Error getting messages for chat {chat_id} (with filter): {e2}")
                        return []
                else:
                    print(f"Error getting messages for chat {chat_id}: {e}")
                    return []
        except Exception as e:
            print(f"Unexpected error getting messages for chat {chat_id}: {e}")
            return []
    
    def get_teams_summary(self, access_token: str) -> TeamsSummary:
        """Get comprehensive Teams summary"""
        try:
            # Get user's teams
            teams = self.get_user_teams(access_token)
            
            all_channels = []
            all_messages = []
            
            # Get channels and messages for each team
            for team in teams:
                team_id = team["id"]
                channels = self.get_team_channels(access_token, team_id)
                
                for channel in channels:
                    channel["team_name"] = team["displayName"]
                    channel["team_id"] = team_id
                    all_channels.append(channel)
                    
                    # Get messages for this channel
                    messages = self.get_channel_messages(access_token, team_id, channel["id"])
                    for message in messages:
                        message["channel_name"] = channel["displayName"]
                        message["team_name"] = team["displayName"]
                    all_messages.extend(messages)
            
            # Get personal chats
            chats = self.get_chats(access_token)
            for chat in chats:
                try:
                    chat_messages = self.get_chat_messages(access_token, chat["id"])
                    for message in chat_messages:
                        message["chat_name"] = chat.get("topic", "Personal Chat")
                        message["is_personal_chat"] = True
                    all_messages.extend(chat_messages)
                except Exception as e:
                    print(f"Error processing chat {chat.get('id', 'unknown')}: {e}")
                    continue
            
            return TeamsSummary(
                channels=all_channels,
                messages=all_messages,
                total_channels=len(all_channels),
                total_messages=len(all_messages),
                total_teams=len(teams),
                summary="Teams data loaded successfully"
            )
            
        except Exception as e:
            raise Exception(f"Failed to get Teams summary: {str(e)}")
    
    def get_all_teams_data(self, access_token: str) -> Dict:
        """Get all Teams data for AI processing"""
        try:
            teams = self.get_user_teams(access_token)
            all_channels = []
            all_messages = []
            
            # Get channels and messages for each team
            for team in teams:
                team_id = team["id"]
                channels = self.get_team_channels(access_token, team_id)
                
                for channel in channels:
                    channel["team_name"] = team["displayName"]
                    channel["team_id"] = team_id
                    all_channels.append(channel)
                    
                    # Get messages for this channel
                    messages = self.get_channel_messages(access_token, team_id, channel["id"])
                    for message in messages:
                        message["channel_name"] = channel["displayName"]
                        message["team_name"] = team["displayName"]
                    all_messages.extend(messages)
            
            # Get personal chats
            chats = self.get_chats(access_token)
            for chat in chats:
                try:
                    chat_messages = self.get_chat_messages(access_token, chat["id"])
                    for message in chat_messages:
                        message["chat_name"] = chat.get("topic", "Personal Chat")
                        message["is_personal_chat"] = True
                    all_messages.extend(chat_messages)
                except Exception as e:
                    print(f"Error processing chat {chat.get('id', 'unknown')}: {e}")
                    continue
            
            return {
                "teams": teams,
                "channels": all_channels,
                "messages": all_messages,
                "total_teams": len(teams),
                "total_channels": len(all_channels),
                "total_messages": len(all_messages),
                "total_chats": len(chats)
            }
            
        except Exception as e:
            raise Exception(f"Failed to get all Teams data: {str(e)}")
    
    def get_user_meetings(self, access_token: str, days_back: int = 30) -> List[Dict]:
        """Get user's meetings and events"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Get meetings from the last N days
            from datetime import datetime, timedelta
            start_date = (datetime.now() - timedelta(days=days_back)).isoformat() + "Z"
            end_date = (datetime.now() + timedelta(days=30)).isoformat() + "Z"
            
            # Get calendar events (which include meetings)
            response = requests.get(
                f"{self.base_url}/me/calendarView",
                headers=headers,
                params={
                    "startDateTime": start_date,
                    "endDateTime": end_date,
                    "$orderby": "start/dateTime",
                    "$top": 100
                }
            )
            response.raise_for_status()
            events = response.json().get("value", [])
            
            # Filter for Teams meetings
            meetings = []
            for event in events:
                if event.get("isOnlineMeeting", False) or "teams" in event.get("onlineMeeting", {}).get("joinUrl", "").lower():
                    meetings.append({
                        "id": event.get("id"),
                        "subject": event.get("subject", "No Subject"),
                        "start": event.get("start", {}).get("dateTime"),
                        "end": event.get("end", {}).get("dateTime"),
                        "organizer": event.get("organizer", {}).get("emailAddress", {}).get("name"),
                        "attendees": [attendee.get("emailAddress", {}).get("name") for attendee in event.get("attendees", [])],
                        "isOnlineMeeting": event.get("isOnlineMeeting", False),
                        "joinUrl": event.get("onlineMeeting", {}).get("joinUrl"),
                        "body": event.get("body", {}).get("content", "")
                    })
            
            return meetings
        except requests.exceptions.RequestException as e:
            print(f"Error getting meetings: {e}")
            return []
    
    def get_meeting_details(self, access_token: str, meeting_id: str) -> Dict:
        """Get detailed information about a specific meeting"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.base_url}/me/events/{meeting_id}", headers=headers)
            response.raise_for_status()
            event = response.json()
            
            return {
                "id": event.get("id"),
                "subject": event.get("subject", "No Subject"),
                "start": event.get("start", {}).get("dateTime"),
                "end": event.get("end", {}).get("dateTime"),
                "organizer": event.get("organizer", {}).get("emailAddress", {}).get("name"),
                "attendees": [attendee.get("emailAddress", {}).get("name") for attendee in event.get("attendees", [])],
                "isOnlineMeeting": event.get("isOnlineMeeting", False),
                "joinUrl": event.get("onlineMeeting", {}).get("joinUrl"),
                "body": event.get("body", {}).get("content", ""),
                "location": event.get("location", {}).get("displayName"),
                "description": event.get("body", {}).get("content", "")
            }
        except requests.exceptions.RequestException as e:
            print(f"Error getting meeting details: {e}")
            return {}
    
    def get_meeting_attendance(self, access_token: str, meeting_id: str) -> List[Dict]:
        """Get attendance report for a meeting (if available)"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.base_url}/me/onlineMeetings/{meeting_id}/attendanceReport", headers=headers)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting meeting attendance: {e}")
            return []
    
    def get_user_info(self, token: str) -> Dict:
        """Get Microsoft Teams user information"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get user info: {str(e)}") 