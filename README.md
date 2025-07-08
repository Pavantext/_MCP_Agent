# MCP Multi-Service Dashboard API

A comprehensive FastAPI application that provides AI-powered dashboards for both Outlook Email and GitHub repositories. The application features intelligent summarization, chatbot assistance, and modern UI design.

## Features

### 🔐 Multi-Service Authentication
- **Microsoft Outlook OAuth**: Secure email access with Microsoft Graph API
- **GitHub OAuth**: Repository and activity management with GitHub API
- **Unified Dashboard**: Choose between Outlook and GitHub services

### 📧 Outlook Email Features
- **AI-Powered Email Summarization**: Intelligent analysis of email content
- **Email Statistics**: Total and unread email counts
- **Email Assistant Chatbot**: Ask questions about your emails
- **Real-time Refresh**: Auto-updating dashboard with latest data

### 🐙 GitHub Features
- **Repository Analysis**: Comprehensive overview of your repositories
- **Issue & PR Tracking**: Monitor open issues and pull requests
- **Activity Insights**: Recent GitHub activity analysis
- **GitHub Assistant Chatbot**: Get insights about your GitHub data
- **Language Statistics**: Programming language distribution

### 🤖 AI Integration
- **Google Gemini AI**: Advanced natural language processing
- **Intelligent Summarization**: Context-aware data analysis
- **Smart Chatbots**: Service-specific AI assistants
- **Pattern Recognition**: Identify trends and insights

## Quick Start

### 1. Environment Setup

Create a `.env` file with your API keys:

```bash
# Microsoft OAuth (for Outlook)
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# AI Service
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

Visit `http://localhost:8000` to access the application.

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth` | GET | Service selection page |
| `/auth/microsoft` | GET | Microsoft OAuth redirect |
| `/auth/github` | GET | GitHub OAuth redirect |
| `/auth/callback` | GET | Microsoft OAuth callback |
| `/auth/github/callback` | GET | GitHub OAuth callback |
| `/auth/logout` | GET | Logout user |

### Outlook Email API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/emails/dashboard` | GET | Email dashboard page |
| `/emails/summary` | GET | Get email summary |
| `/emails/all` | GET | Get all emails |
| `/emails/unread` | GET | Get unread emails |
| `/chatbot/suggestions` | GET | Get email chatbot suggestions |
| `/chatbot/chat` | POST | Process email chatbot message |

### GitHub API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/github/dashboard` | GET | GitHub dashboard page |
| `/github/summary` | GET | Get GitHub summary |
| `/github/repositories` | GET | Get user repositories |
| `/github/issues` | GET | Get user issues |
| `/github/pull-requests` | GET | Get user pull requests |
| `/github/activity` | GET | Get user activity |
| `/github/chatbot/suggestions` | GET | Get GitHub chatbot suggestions |
| `/github/chatbot/chat` | POST | Process GitHub chatbot message |

## Integration Examples

### JavaScript Integration

```javascript
// Get email summary
const response = await fetch('/emails/summary', {
    headers: { 'Authorization': 'Bearer your_token' }
});
const data = await response.json();

// Get GitHub repositories
const githubResponse = await fetch('/github/repositories', {
    headers: { 'Authorization': 'Bearer your_token' }
});
const githubData = await githubResponse.json();

// Chat with email assistant
const chatResponse = await fetch('/chatbot/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'How many unread emails do I have?' })
});
const chatData = await chatResponse.json();
```

### Python Integration

```python
import requests

# Get email summary
response = requests.get('/emails/summary', headers={'Authorization': 'Bearer your_token'})
email_summary = response.json()

# Get GitHub data
github_response = requests.get('/github/repositories', headers={'Authorization': 'Bearer your_token'})
repositories = github_response.json()

# Chat with assistant
chat_response = requests.post('/chatbot/chat', 
    json={'message': 'Show me my recent activity'},
    headers={'Content-Type': 'application/json'})
chat_data = chat_response.json()
```

### cURL Examples

```bash
# Get email summary
curl -X GET "http://localhost:8000/emails/summary" \
  -H "Authorization: Bearer your_token"

# Get GitHub repositories
curl -X GET "http://localhost:8000/github/repositories" \
  -H "Authorization: Bearer your_token"

# Chat with assistant
curl -X POST "http://localhost:8000/chatbot/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How many repositories do I have?"}'
```

### React Integration

```jsx
import React, { useState, useEffect } from 'react';

function Dashboard() {
    const [emailSummary, setEmailSummary] = useState(null);
    const [githubData, setGithubData] = useState(null);

    useEffect(() => {
        // Fetch email summary
        fetch('/emails/summary')
            .then(res => res.json())
            .then(data => setEmailSummary(data));

        // Fetch GitHub data
        fetch('/github/repositories')
            .then(res => res.json())
            .then(data => setGithubData(data));
    }, []);

    const sendMessage = async (message) => {
        const response = await fetch('/chatbot/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        return response.json();
    };

    return (
        <div>
            <h1>Dashboard</h1>
            {/* Render your dashboard components */}
        </div>
    );
}
```

## Authentication Flow

### Microsoft OAuth (Outlook)

1. User visits `/auth`
2. Clicks "Outlook Email" button
3. Redirected to Microsoft OAuth
4. User authorizes the application
5. Redirected back to `/auth/callback`
6. Access token stored in session
7. Redirected to `/dashboard` (Outlook dashboard)

### GitHub OAuth

1. User visits `/auth`
2. Clicks "GitHub" button
3. Redirected to GitHub OAuth
4. User authorizes the application
5. Redirected back to `/auth/github/callback`
6. Access token stored in session
7. Redirected to `/github/dashboard`

## Error Handling

The API includes comprehensive error handling:

```json
{
    "detail": "Error message",
    "status_code": 400
}
```

Common error codes:
- `401`: Authentication required
- `400`: Bad request
- `500`: Internal server error

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MICROSOFT_CLIENT_ID` | Microsoft OAuth client ID | Yes (for Outlook) |
| `MICROSOFT_CLIENT_SECRET` | Microsoft OAuth client secret | Yes (for Outlook) |
| `GITHUB_CLIENT_ID` | GitHub OAuth client ID | Yes (for GitHub) |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth client secret | Yes (for GitHub) |
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes (for AI features) |

## Development

### Project Structure

```
_MCP_Agent/
├── api/
│   ├── models/
│   │   ├── email.py
│   │   ├── chatbot.py
│   │   └── github.py
│   ├── routers/
│   │   ├── email_router.py
│   │   ├── chatbot_router.py
│   │   ├── auth_router.py
│   │   └── github_router.py
│   ├── services/
│   │   ├── email_service.py
│   │   ├── email_ai_service.py
│   │   ├── chatbot_service.py
│   │   ├── github_service.py
│   │   ├── github_ai_service.py
│   │   └── github_chatbot_service.py
│   └── auth.py
├── frontend/
│   └── templates/
│       ├── dashboard.html
│       └── github_dashboard.html
├── main.py
├── requirements.txt
└── README.md
```

### Adding New Services

1. Create service models in `api/models/`
2. Create service logic in `api/services/`
3. Create API router in `api/routers/`
4. Add authentication in `api/auth.py`
5. Create dashboard template in `frontend/templates/`
6. Update main.py to include new router

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.