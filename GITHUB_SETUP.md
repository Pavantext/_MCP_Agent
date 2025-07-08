# GitHub Integration Setup Guide

This guide explains how to set up the GitHub integration feature in your MCP Outlook Reader application.

## Environment Variables Required

Add these environment variables to your `.env` file:

```bash
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
GITHUB_SCOPES=repo user

# Google AI API (for GitHub summaries)
GEMINI_API_KEY=your_gemini_api_key_here
```

## Setting up GitHub OAuth

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the application details:
   - **Application name**: MCP Outlook Reader
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/auth/github/callback`
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret** to your `.env` file

## Features Added

### 1. GitHub Authentication
- OAuth flow for GitHub authentication
- Secure token storage
- Automatic token validation

### 2. GitHub Data Fetching
- **Repositories**: Get all user repositories with details
- **Commits**: Recent commits from all repositories
- **Issues**: User's issues across all repositories
- **Pull Requests**: User's pull requests

### 3. AI-Powered GitHub Summary
- Comprehensive analysis of GitHub activity
- Repository statistics and trends
- Programming language analysis
- Development activity patterns

### 4. GitHub Chatbot
- Ask questions about your GitHub data
- Get insights about repositories, commits, issues
- Analyze development patterns
- Find specific information quickly

### 5. Dashboard Integration
- "Analyze My GitHub" button
- Separate GitHub summary card
- GitHub chatbot interface
- Real-time data refresh

## API Endpoints

### GitHub Authentication
- `GET /github/login` - Start GitHub OAuth flow
- `GET /auth/github/callback` - Handle OAuth callback
- `GET /github/status` - Check authentication status
- `POST /github/logout` - Logout from GitHub

### GitHub Data
- `GET /github/summary` - Get basic GitHub summary
- `GET /github/repositories` - Get all repositories
- `GET /github/commits` - Get recent commits
- `GET /github/issues` - Get user issues
- `GET /github/pull-requests` - Get user pull requests
- `GET /github/ai-summary` - Get AI-powered summary

### GitHub Chatbot
- `POST /github-chatbot/chat` - Chat with GitHub assistant
- `GET /github-chatbot/suggestions` - Get suggested questions

## Usage

1. Start the application: `python app.py`
2. Navigate to `http://localhost:8000`
3. Authenticate with Microsoft (for emails)
4. Click "🐙 Analyze My GitHub" button
5. Authenticate with GitHub
6. View your GitHub summary and chat with the assistant

## Code Structure

```
api/
├── models/
│   └── github.py              # GitHub data models
├── routers/
│   ├── github.py              # GitHub API endpoints
│   └── github_chatbot.py      # GitHub chatbot endpoints
├── services/
│   ├── github_auth_service.py # GitHub OAuth handling
│   ├── github_service.py      # GitHub API data fetching
│   └── github_chatbot_service.py # GitHub AI chatbot
└── main.py                    # Updated with GitHub routes

frontend/
└── templates/
    └── dashboard.html         # Updated with GitHub UI
```

## Security Notes

- Tokens are stored in memory (for development)
- In production, use a proper database for token storage
- Implement proper session management
- Add rate limiting for API calls
- Validate all user inputs

## Troubleshooting

1. **GitHub authentication fails**: Check your OAuth app settings and environment variables
2. **No data appears**: Ensure your GitHub account has repositories and activity
3. **AI summary fails**: Check your Google API key and quota
4. **Rate limiting**: GitHub API has rate limits; the app handles this gracefully

## Future Enhancements

- Add GitHub webhook support for real-time updates
- Implement repository-specific analytics
- Add GitHub Actions workflow analysis
- Support for GitHub Enterprise
- Export GitHub data to various formats 