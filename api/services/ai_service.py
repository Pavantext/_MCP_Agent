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
        
        # Prepare email data for AI
        email_texts = []
        for email in emails[:20]:  # Limit to 20 emails for AI processing
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            body_preview = email.get("bodyPreview", "")
            received = email.get("receivedDateTime", "Unknown")
            
            email_text = f"""
From: {from_info}
Subject: {subject}
Received: {received}
Preview: {body_preview}
---
"""
            email_texts.append(email_text)
        
        # Create prompt for AI
        prompt = f"""
You are an AI assistant that summarizes emails. Please provide a concise, well-organized summary of the following {len(email_texts)} unread emails.

Focus on:
1. Key themes and topics
2. Important senders
3. Urgent or time-sensitive items
4. Overall email volume and patterns

Here are the emails:

{''.join(email_texts)}

Please provide a clear, structured summary that helps the user quickly understand their unread emails.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI summary: {str(e)}")
            return self._fallback_summary(emails)
    
    def _fallback_summary(self, emails: List[Dict]) -> str:
        """Fallback summary when AI fails"""
        summary_parts = []
        summary_parts.append(f"📧 Email Summary ({len(emails)} unread emails)")
        summary_parts.append("=" * 50)
        
        for i, email in enumerate(emails[:10], 1):
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            
            summary_parts.append(f"{i}. {from_info}: {subject}")
        
        if len(emails) > 10:
            summary_parts.append(f"... and {len(emails) - 10} more emails")
        
        return "\n".join(summary_parts) 