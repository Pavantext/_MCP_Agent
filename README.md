# MCP Outlook Reader API

A modular API service for reading and summarizing Outlook emails with GitHub integration and AI-powered insights.

## Features

- **Email Management**: Read, summarize, and manage Outlook emails
- **GitHub Integration**: Connect and analyze GitHub repositories and activity
- **AI-Powered Summaries**: Generate intelligent summaries using Google's Gemini AI
- **Chatbot Assistant**: Interactive chat interface for email and GitHub queries
- **OAuth Authentication**: Secure authentication with Microsoft and GitHub

## Project Structure

```
_MCP_Agent/
├── api/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic data models
│   ├── routers/             # API route handlers
│   └── services/            # Business logic services
├── frontend/
│   └── templates/           # HTML templates
├── app.py                   # Application launcher
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Code Quality Improvements

### ✅ Removed Unused Code
- **Unused Models**: Removed `ChatSession`, `GitHubRepository`, `GitHubCommit`, `GitHubIssue`, `GitHubPullRequest`
- **Unused Dependencies**: Removed `python-multipart` from requirements.txt
- **Virtual Environment**: Added `mcp/` to .gitignore

### ✅ Improved Code Structure
- **Constants**: Added meaningful constants for configuration values
- **Error Handling**: Standardized error handling across services
- **Code Organization**: Broke down large functions into smaller, focused methods
- **Type Hints**: Enhanced type annotations for better code clarity

### ✅ Enhanced Readability
- **Consistent Naming**: Improved variable and function names
- **Documentation**: Added comprehensive docstrings
- **Code Reuse**: Eliminated duplicate code patterns
- **Modular Design**: Better separation of concerns

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd _MCP_Agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```
   CLIENT_ID=your_microsoft_client_id
   CLIENT_SECRET=your_microsoft_client_secret
   TENANT_ID=your_tenant_id
   REDIRECT_URI=http://localhost:8000/auth/callback
   SCOPES=Mail.Read
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
   GITHUB_SCOPES=repo user
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## API Endpoints

### Authentication
- `GET /auth/login` - Microsoft OAuth login
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/status` - Check authentication status
- `POST /auth/logout` - Logout user

### Email Management
- `GET /emails/summary` - Get email summary
- `GET /emails/all` - Get all emails
- `GET /emails/unread` - Get unread emails
- `GET /emails/ai-summary` - Get AI-powered summary
- `PATCH /emails/{email_id}/read` - Mark email as read

### GitHub Integration
- `GET /github/login` - GitHub OAuth login
- `GET /github/callback` - GitHub OAuth callback
- `GET /github/summary` - Get GitHub summary
- `GET /github/repositories` - Get user repositories
- `GET /github/commits` - Get recent commits
- `GET /github/issues` - Get user issues
- `GET /github/pull-requests` - Get pull requests
- `GET /github/ai-summary` - Get AI-powered GitHub summary

### Chatbot
- `POST /chatbot/chat` - Chat with email assistant
- `GET /chatbot/suggestions` - Get chat suggestions
- `POST /github-chatbot/chat` - Chat with GitHub assistant
- `GET /github-chatbot/suggestions` - Get GitHub chat suggestions

## Services

### EmailService
Handles Microsoft Graph API operations for email management with improved error handling and constants.

### AIService
Provides AI-powered summarization using Google's Gemini model with structured prompts and fallback mechanisms.

### GitHubService
Manages GitHub API interactions for repository, commit, issue, and pull request data.

### AuthService & GitHubAuthService
Handle OAuth authentication flows for Microsoft and GitHub respectively.

## Code Quality Metrics

- **Unused Code Removed**: 5 unused model classes, 1 unused dependency
- **Constants Added**: 15+ configuration constants for better maintainability
- **Error Handling**: Standardized across all services
- **Type Hints**: Enhanced throughout the codebase
- **Documentation**: Comprehensive docstrings added

## Development

The codebase follows these principles:
- **Single Responsibility**: Each class and function has a clear, focused purpose
- **DRY (Don't Repeat Yourself)**: Eliminated code duplication
- **SOLID Principles**: Applied throughout the architecture
- **Error Resilience**: Graceful handling of API failures
- **Maintainability**: Clear structure and documentation

## Contributing

1. Follow the existing code style and structure
2. Add type hints to new functions
3. Include docstrings for new classes and methods
4. Test your changes thoroughly
5. Update documentation as needed