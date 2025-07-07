import requests
from typing import List, Dict, Optional
from ..models.auth import EmailSummary


class EmailService:
    """Service for handling Microsoft Graph email operations"""
    
    def __init__(self):
        self.base_url = "https://graph.microsoft.com/v1.0"
    
    def get_all_emails(self, access_token: str) -> List[Dict]:
        """Get all emails from Microsoft Graph API"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Query for all emails
        params = {
            "$top": 100,  # Limit to 100 emails
            "$orderby": "receivedDateTime desc",
            "$select": "subject,from,receivedDateTime,bodyPreview,id,isRead"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/me/messages",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("value", [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching emails: {str(e)}")
            return []
    
    def get_email_summary(self, access_token: str) -> EmailSummary:
        """Get a summary of all emails"""
        emails = self.get_all_emails(access_token)
        
        if not emails:
            return EmailSummary(
                summary="No emails found.",
                email_count=0
            )
        
        # Count unread emails
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        
        # Create a simple summary
        summary_parts = []
        summary_parts.append(f"Found {len(emails)} total email(s) ({unread_count} unread):\n")
        
        for i, email in enumerate(emails[:10], 1):  # Show first 10 emails
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            received = email.get("receivedDateTime", "Unknown")
            is_read = email.get("isRead", True)
            status = "📬" if not is_read else "📭"
            
            summary_parts.append(f"{i}. {status} From: {from_info}")
            summary_parts.append(f"   Subject: {subject}")
            summary_parts.append(f"   Received: {received}")
            summary_parts.append("")
        
        if len(emails) > 10:
            summary_parts.append(f"... and {len(emails) - 10} more emails")
        
        return EmailSummary(
            summary="\n".join(summary_parts),
            email_count=len(emails)
        )
    
    def get_unread_emails(self, access_token: str) -> List[Dict]:
        """Get unread emails from Microsoft Graph API"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Query for unread emails
        params = {
            "$filter": "isRead eq false",
            "$top": 50,  # Limit to 50 emails
            "$orderby": "receivedDateTime desc",
            "$select": "subject,from,receivedDateTime,bodyPreview,id"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/me/messages",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("value", [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching unread emails: {str(e)}")
            return []
    
    def mark_as_read(self, access_token: str, email_id: str) -> bool:
        """Mark an email as read"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "isRead": True
        }
        
        try:
            response = requests.patch(
                f"{self.base_url}/me/messages/{email_id}",
                headers=headers,
                json=data
            )
            return response.status_code == 200
        except:
            return False 