# MCP Outlook Reader

A modular API service for reading and summarizing Outlook emails using Microsoft Graph API and AI-powered summarization.

## 🏗️ Project Structure

```
_MCP_Agent/
├── api/                    # API backend
│   ├── main.py            # Main FastAPI application
│   ├── models/            # Pydantic models
│   │   └── auth.py
│   ├── routers/           # API routes
│   │   ├── auth.py        # Authentication routes
│   │   └── emails.py      # Email routes
│   └── services/          # Business logic
│       ├── auth_service.py    # Microsoft OAuth
│       ├── email_service.py   # Email operations
│       └── ai_service.py      # AI summarization
├── frontend/              # Frontend templates
│   └── templates/
│       └── dashboard.html
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables
```

## 🚀 Features

- **🔐 Microsoft OAuth Authentication** - Secure login with Microsoft accounts
- **📧 Email Reading** - Fetch unread emails from Outlook
- **🤖 AI Summarization** - Powered by Google Gemini AI
- **📊 Beautiful Dashboard** - Modern, responsive web interface
- **🔌 RESTful API** - Modular API for external integrations
- **📱 Responsive Design** - Works on desktop and mobile

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd _MCP_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with:
   ```env
   # Microsoft OAuth Configuration
   CLIENT_ID=your_client_id_here
   TENANT_ID=your_tenant_id_here
   REDIRECT_URI=http://127.0.0.1:8000/auth/callback
   SCOPES=https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read
   
   # AI Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Configure Azure App Registration**
   - Go to Azure Portal → App Registrations
   - Create a new app or use existing one
   - Add redirect URI: `http://127.0.0.1:8000/auth/callback`
   - Add API permissions: `Mail.Read`, `User.Read`
   - Copy Application ID → `CLIENT_ID`
   - Copy Directory ID → `TENANT_ID`

## 🚀 Running the Application

### Development Mode
```bash
python app.py
```

### Production Mode
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 📡 API Documentation

### Authentication Endpoints

#### `GET /auth/login`
Redirects user to Microsoft OAuth login page.

**Response:** Redirect to Microsoft login

#### `GET /auth/callback?code={auth_code}`
Handles OAuth callback and stores access token.

**Response:** Redirect to dashboard

#### `GET /auth/status`
Check if user is authenticated.

**Response:**
```json
{
  "is_authenticated": true,
  "message": "User is authenticated"
}
```

#### `POST /auth/logout`
Logout user and clear session.

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

#### `GET /auth/token`
Get current access token (for API usage).

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer"
}
```

### Email Endpoints

#### `GET /emails/summary`
Get basic email summary with statistics.

**Response:**
```json
{
  "summary": "Found 25 total email(s) (5 unread):\n1. 📬 John Doe: Meeting tomorrow\n...",
  "email_count": 25,
  "status": "success"
}
```

#### `GET /emails/unread`
Get list of unread emails.

**Response:**
```json
[
  {
    "id": "AAMkAGVmMDEzMTM4LTZmYWUtNDdkNC1hMDZkL...",
    "subject": "Meeting tomorrow",
    "from": {
      "emailAddress": {
        "name": "John Doe",
        "address": "john@example.com"
      }
    },
    "receivedDateTime": "2024-01-15T10:30:00Z",
    "bodyPreview": "Hi, let's meet tomorrow at 2 PM...",
    "isRead": false
  }
]
```

#### `GET /emails/all`
Get list of all emails (up to 100 most recent).

**Response:** Same format as `/emails/unread` but includes all emails.

#### `GET /emails/ai-summary`
Get AI-powered email summary and analysis.

**Response:**
```json
{
  "summary": "<h2>📧 Email Summary</h2><p><strong>Key Themes:</strong>...</p>",
  "email_count": 25,
  "unread_count": 5,
  "status": "success"
}
```

#### `PATCH /emails/{email_id}/read`
Mark a specific email as read.

**Response:**
```json
{
  "message": "Email marked as read"
}
```

### Chatbot Endpoints

#### `POST /chatbot/chat`
Send a message to the email assistant.

**Request:**
```json
{
  "message": "How many unread emails do I have?"
}
```

**Response:**
```json
{
  "response": "<h3>Email Analysis</h3><p>You have <strong>5 unread emails</strong> out of 25 total emails.</p>",
  "status": "success",
  "message_count": 25
}
```

#### `GET /chatbot/suggestions`
Get suggested questions for the chatbot.

**Response:**
```json
{
  "suggestions": [
    "How many unread emails do I have?",
    "Show me emails from a specific sender",
    "What are the most recent emails?",
    "Are there any urgent emails?",
    "Summarize my emails by topic",
    "Find emails about meetings",
    "What's my email activity pattern?",
    "Which senders email me most often?"
  ]
}
```

### Web Interface Endpoints

#### `GET /`
Main entry point - redirects to login or dashboard based on authentication.

#### `GET /dashboard`
Email summary dashboard with AI analysis and chatbot.

#### `GET /docs`
Interactive API documentation (Swagger UI).

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "MCP Outlook Reader API"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLIENT_ID` | Azure App Registration Client ID | Yes |
| `TENANT_ID` | Azure Directory (Tenant) ID | Yes |
| `REDIRECT_URI` | OAuth redirect URI | Yes |
| `SCOPES` | Microsoft Graph API scopes | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

## 🔌 Integration Guide

### Using the API in Other Projects

The MCP Outlook Reader API can be easily integrated into other applications. Here are examples for different programming languages:

#### JavaScript/Node.js Example

```javascript
// Get email summary
async function getEmailSummary() {
    const response = await fetch('http://localhost:8000/emails/ai-summary', {
        headers: {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
    });
    const data = await response.json();
    console.log('Email Summary:', data.summary);
}

// Chat with email assistant
async function askEmailAssistant(question) {
    const response = await fetch('http://localhost:8000/chatbot/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        },
        body: JSON.stringify({
            message: question
        })
    });
    const data = await response.json();
    console.log('Assistant Response:', data.response);
}

// Get unread emails
async function getUnreadEmails() {
    const response = await fetch('http://localhost:8000/emails/unread', {
        headers: {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
    });
    const emails = await response.json();
    console.log('Unread Emails:', emails);
}
```

#### Python Example

```python
import requests

class EmailAPI:
    def __init__(self, base_url="http://localhost:8000", access_token=None):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {access_token}' if access_token else None
        }
    
    def get_email_summary(self):
        """Get AI-powered email summary"""
        response = requests.get(f"{self.base_url}/emails/ai-summary", headers=self.headers)
        return response.json()
    
    def get_unread_emails(self):
        """Get list of unread emails"""
        response = requests.get(f"{self.base_url}/emails/unread", headers=self.headers)
        return response.json()
    
    def chat_with_assistant(self, message):
        """Send message to email assistant"""
        response = requests.post(
            f"{self.base_url}/chatbot/chat",
            headers={**self.headers, 'Content-Type': 'application/json'},
            json={'message': message}
        )
        return response.json()
    
    def mark_email_as_read(self, email_id):
        """Mark email as read"""
        response = requests.patch(
            f"{self.base_url}/emails/{email_id}/read",
            headers=self.headers
        )
        return response.json()

# Usage example
api = EmailAPI(access_token="your_access_token_here")

# Get email summary
summary = api.get_email_summary()
print(summary['summary'])

# Ask assistant
response = api.chat_with_assistant("How many unread emails do I have?")
print(response['response'])
```

#### cURL Examples

```bash
# Get email summary
curl -X GET "http://localhost:8000/emails/ai-summary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Chat with assistant
curl -X POST "http://localhost:8000/chatbot/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"message": "How many unread emails do I have?"}'

# Get unread emails
curl -X GET "http://localhost:8000/emails/unread" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Mark email as read
curl -X PATCH "http://localhost:8000/emails/EMAIL_ID/read" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### React/JavaScript Frontend Example

```jsx
import React, { useState, useEffect } from 'react';

function EmailDashboard() {
    const [emails, setEmails] = useState([]);
    const [summary, setSummary] = useState('');
    const [chatResponse, setChatResponse] = useState('');
    
    // Get email summary
    const fetchEmailSummary = async () => {
        try {
            const response = await fetch('/emails/ai-summary');
            const data = await response.json();
            setSummary(data.summary);
        } catch (error) {
            console.error('Error fetching summary:', error);
        }
    };
    
    // Chat with assistant
    const askAssistant = async (question) => {
        try {
            const response = await fetch('/chatbot/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: question })
            });
            const data = await response.json();
            setChatResponse(data.response);
        } catch (error) {
            console.error('Error chatting with assistant:', error);
        }
    };
    
    useEffect(() => {
        fetchEmailSummary();
    }, []);
    
    return (
        <div>
            <h1>Email Dashboard</h1>
            <div dangerouslySetInnerHTML={{ __html: summary }} />
            <button onClick={() => askAssistant('How many unread emails?')}>
                Ask Assistant
            </button>
            <div dangerouslySetInnerHTML={{ __html: chatResponse }} />
        </div>
    );
}
```

### Authentication Flow

To use the API in other projects, you'll need to handle authentication:

1. **Redirect users to login:**
   ```
   GET http://localhost:8000/auth/login
   ```

2. **Handle OAuth callback:**
   ```
   GET http://localhost:8000/auth/callback?code=AUTH_CODE
   ```

3. **Get access token:**
   ```
   GET http://localhost:8000/auth/token
   ```

4. **Use token in API calls:**
   ```javascript
   headers: {
       'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
   }
   ```

### Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `401` - Not authenticated
- `400` - Bad request
- `500` - Server error

Error responses include details:
```json
{
  "detail": "Error message here"
}
```

### Azure App Registration Setup

1. **Create App Registration**
   - Go to Azure Portal → Azure Active Directory → App registrations
   - Click "New registration"
   - Name: "MCP Outlook Reader"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: Web → `http://127.0.0.1:8000/auth/callback`

2. **Configure API Permissions**
   - Go to API permissions
   - Add Microsoft Graph permissions:
     - `Mail.Read` (delegated)
     - `User.Read` (delegated)
   - Grant admin consent

3. **Get Configuration Values**
   - Application (client) ID → `CLIENT_ID`
   - Directory (tenant) ID → `TENANT_ID`

## 🎨 Frontend Features

- **Responsive Design** - Works on all devices
- **Real-time Updates** - Auto-refresh every 5 minutes
- **Interactive Dashboard** - Beautiful email summary display
- **Error Handling** - Graceful error messages
- **Loading States** - Smooth user experience

## 🔒 Security

- **OAuth 2.0** - Secure Microsoft authentication
- **Token Validation** - Automatic token validation
- **HTTPS Ready** - Production-ready security
- **Input Validation** - Pydantic model validation

## 📈 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] Email filtering and search
- [ ] Email categorization
- [ ] Notification system
- [ ] Multi-user support
- [ ] Advanced AI features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Verify your Azure configuration
4. Ensure all environment variables are set correctly