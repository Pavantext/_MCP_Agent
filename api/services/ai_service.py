import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """Service for AI-powered email summarization"""
    
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