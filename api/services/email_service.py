import requests
from typing import List, Dict, Optional
from ..models.auth import EmailSummary

# Constants
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"
DEFAULT_EMAIL_LIMIT = 100
DEFAULT_UNREAD_LIMIT = 50
MAX_EMAILS_FOR_SUMMARY = 10
MAX_EMAILS_FOR_AI = 30

class EmailService:
    """Service for handling Microsoft Graph email operations"""
    
    def __init__(self):
        self.base_url = GRAPH_API_BASE_URL
    
    def _get_headers(self, access_token: str) -> Dict[str, str]:
        """Get headers with authentication token"""
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, url: str, headers: Dict[str, str], params: Optional[Dict] = None) -> Dict:
        """Make HTTP request with error handling"""
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                raise Exception("401 Unauthorized")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            raise
    
    def get_all_emails(self, access_token: str) -> List[Dict]:
        """Get all emails from Microsoft Graph API"""
        headers = self._get_headers(access_token)
        
        # Query for all emails
        params = {
            "$top": DEFAULT_EMAIL_LIMIT,
            "$orderby": "receivedDateTime desc",
            "$select": "subject,from,receivedDateTime,bodyPreview,id,isRead"
        }
        
        data = self._make_request(
            f"{self.base_url}/me/messages",
            headers=headers,
            params=params
        )
        
        return data.get("value", [])
    
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
        
        for i, email in enumerate(emails[:MAX_EMAILS_FOR_SUMMARY], 1):
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            received = email.get("receivedDateTime", "Unknown")
            is_read = email.get("isRead", True)
            status = "📬" if not is_read else "📭"
            
            summary_parts.append(f"{i}. {status} From: {from_info}")
            summary_parts.append(f"   Subject: {subject}")
            summary_parts.append(f"   Received: {received}")
            summary_parts.append("")
        
        if len(emails) > MAX_EMAILS_FOR_SUMMARY:
            summary_parts.append(f"... and {len(emails) - MAX_EMAILS_FOR_SUMMARY} more emails")
        
        return EmailSummary(
            summary="\n".join(summary_parts),
            email_count=len(emails)
        )
    
    def get_unread_emails(self, access_token: str) -> List[Dict]:
        """Get unread emails from Microsoft Graph API"""
        headers = self._get_headers(access_token)
        
        # Query for unread emails
        params = {
            "$filter": "isRead eq false",
            "$top": DEFAULT_UNREAD_LIMIT,
            "$orderby": "receivedDateTime desc",
            "$select": "subject,from,receivedDateTime,bodyPreview,id"
        }
        
        data = self._make_request(
            f"{self.base_url}/me/messages",
            headers=headers,
            params=params
        )
        
        return data.get("value", [])
    
    def mark_as_read(self, access_token: str, email_id: str) -> bool:
        """Mark an email as read"""
        headers = self._get_headers(access_token)
        
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
        except requests.exceptions.RequestException:
            return False 