import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def summarize_emails(emails, user_prompt="Summarize my unread emails"):
    context = "\n\n".join(
        [f"Subject: {email['subject']}\nFrom: {email['from']}\nBody: {email['body_preview']}" for email in emails]
    )
    full_prompt = f"{user_prompt}:\n\n{context}"
    response = model.generate_content(full_prompt)
    return response.text
