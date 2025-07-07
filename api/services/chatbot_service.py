import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class ChatbotService:
    """Service for email-related chatbot functionality"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_email_context(self, emails: List[Dict]) -> str:
        """Create context from emails for chatbot"""
        if not emails:
            return "No emails available."
        
        # Prepare email context
        email_contexts = []
        for email in emails[:50]:  # Use up to 50 emails for context
            from_info = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = email.get("subject", "No Subject")
            body_preview = email.get("bodyPreview", "")
            received = email.get("receivedDateTime", "Unknown")
            is_read = email.get("isRead", True)
            status = "UNREAD" if not is_read else "READ"
            
            email_context = f"""
Email {len(email_contexts) + 1}:
Status: {status}
From: {from_info}
Subject: {subject}
Received: {received}
Preview: {body_preview}
"""
            email_contexts.append(email_context)
        
        return "\n".join(email_contexts)
    
    def chat_about_emails(self, user_message: str, emails: List[Dict]) -> str:
        """Generate chatbot response for email-related queries"""
        if not emails:
            return "I don't have access to any emails at the moment. Please check your email connection."
        
        email_context = self.get_email_context(emails)
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        # Create system prompt for email chatbot
        system_prompt = f"""
You are a helpful email assistant chatbot. You have access to {total_count} emails ({unread_count} unread) and can help users with email-related queries.

Your capabilities include:
- Answering questions about specific emails
- Providing email statistics and summaries
- Helping find emails from specific senders
- Identifying urgent or important emails
- Suggesting email management strategies
- Explaining email patterns and trends

Current email context:
{email_context}

User's question: {user_message}

Please provide a helpful, conversational response. Use HTML formatting for better readability:
- Use <strong> for emphasis
- Use <ul> and <li> for lists
- Use <p> for paragraphs
- Use <h3> for section headers if needed

Keep responses concise but informative. If you can't find specific information, be honest about it.
"""
        
        try:
            response = self.model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            print(f"Error generating chatbot response: {str(e)}")
            return self._fallback_response(user_message, emails)
    
    def _fallback_response(self, user_message: str, emails: List[Dict]) -> str:
        """Fallback response when AI fails"""
        unread_count = sum(1 for email in emails if not email.get("isRead", True))
        total_count = len(emails)
        
        return f"""
<h3>Email Assistant Response</h3>
<p>I'm having trouble processing your request right now, but I can tell you about your emails:</p>
<ul>
<li><strong>Total emails:</strong> {total_count}</li>
<li><strong>Unread emails:</strong> {unread_count}</li>
<li><strong>Your question:</strong> {user_message}</li>
</ul>
<p>Please try asking a simpler question or refresh the page to try again.</p>
""" 