# MCP Agent - Multi-Platform Integration Dashboard

A comprehensive dashboard application that integrates Microsoft Outlook emails, GitHub repositories, and Microsoft Teams with AI-powered insights and interactive chatbots.

## 🚀 Features

### 📧 **Email Management**
- Read and summarize Outlook emails
- AI-powered email analysis and insights
- Interactive email assistant chatbot
- Unread email tracking and management

### 🐙 **GitHub Integration**
- Connect and analyze GitHub repositories
- View commits, issues, and pull requests
- AI-powered GitHub activity summaries
- Interactive GitHub assistant chatbot

### 💬 **Microsoft Teams Integration**
- Access Teams channels and messages
- Calendar and meeting management
- AI-powered Teams activity analysis
- Interactive Teams assistant chatbot

### 🤖 **AI-Powered Insights**
- Google Gemini AI integration
- Intelligent data summarization
- Context-aware chatbot responses
- Real-time data analysis

## 📋 Prerequisites

- Python 3.8 or higher
- Microsoft Azure account
- GitHub account
- Google Cloud account (for Gemini AI)
- Modern web browser

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Pavantext/_MCP_Agent.git
cd _MCP_Agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🔑 Platform Setup & API Keys

### Microsoft Azure Setup (Email & Teams)

#### Step 1: Create Azure App Registration
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in details:
   - **Name**: MCP Agent
   - **Supported account types**: Accounts in this organizational directory only (Single tenant)
   - **Redirect URI**: Web - `http://localhost:8000/auth/callback`
5. Click **Register**

#### Step 2: Configure API Permissions
1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add these permissions:
   - `Mail.Read`
   - `User.Read`
   - `Chat.Read`
   - `Chat.ReadWrite`
   - `Channel.ReadBasic.All`
   - `Team.ReadBasic.All`
   - `Calendars.Read`
   - `OnlineMeetings.Read`
6. Click **Grant admin consent**

#### Step 3: Get Credentials
1. Go to **Overview** and copy:
   - **Application (client) ID**
   - **Directory (tenant) ID**
2. Go to **Certificates & secrets**
3. Click **New client secret**
4. Copy the **Value** (client secret)

### GitHub Setup

#### Step 1: Create GitHub OAuth App
1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Fill in details:
   - **Application name**: MCP Agent
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/auth/github/callback`
4. Click **Register application**

#### Step 2: Get GitHub Credentials
1. Copy the **Client ID**
2. Click **Generate a new client secret**
3. Copy the **Client Secret**

### Google Cloud Setup (Gemini AI)

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Generative AI API**

#### Step 2: Get API Key
1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **API Key**
3. Copy the API key

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
# Microsoft Azure Configuration (Email & Teams)
CLIENT_ID=your_azure_client_id_here
CLIENT_SECRET=your_azure_client_secret_here
TENANT_ID=your_azure_tenant_id_here
REDIRECT_URI=http://localhost:8000/auth/callback
SCOPES=Mail.Read User.Read

# Teams Configuration
TEAMS_CLIENT_ID=your_azure_client_id_here
TEAMS_CLIENT_SECRET=your_azure_client_secret_here
TEAMS_TENANT_ID=your_azure_tenant_id_here
TEAMS_REDIRECT_URI=http://localhost:8000/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read

# GitHub Configuration
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
GITHUB_SCOPES=repo user

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🚀 Running the Application

### Start the Server
```bash
python app.py
```

The application will be available at: `http://localhost:8000`

### First Time Setup
1. Open `http://localhost:8000` in your browser
2. Click **Login with Microsoft** to authenticate
3. Grant permissions when prompted
4. You'll be redirected to the dashboard

## 📊 Dashboard Features

### Email Dashboard
- **AI Email Summary**: Intelligent analysis of your emails
- **Email Assistant**: Chat with AI about your emails
- **Email Statistics**: Total and unread email counts
- **Quick Actions**: View all emails or unread only

### GitHub Dashboard
- **AI GitHub Summary**: Analysis of your repositories and activity
- **GitHub Assistant**: Chat with AI about your GitHub data
- **Repository Stats**: Total repositories and recent activity
- **Connect Button**: Authenticate with GitHub

### Teams Dashboard
- **AI Teams Summary**: Analysis of your Teams activity
- **Teams Assistant**: Chat with AI about your Teams data
- **Teams Stats**: Total teams, channels, and meetings
- **Connect Button**: Authenticate with Microsoft Teams

## 🔌 API Endpoints

### Authentication
```http
GET /auth/login                    # Microsoft OAuth login
GET /auth/callback                 # OAuth callback handler
GET /auth/status                   # Check authentication status
POST /auth/logout                  # Logout user
```

### Email Management
```http
GET /emails/summary               # Get email summary
GET /emails/all                   # Get all emails
GET /emails/unread                # Get unread emails
GET /emails/ai-summary            # Get AI-powered summary
PATCH /emails/{email_id}/read     # Mark email as read
```

### GitHub Integration
```http
GET /github/login                 # GitHub OAuth login
GET /github/callback              # GitHub OAuth callback
GET /github/status                # Check GitHub auth status
GET /github/summary               # Get GitHub summary
GET /github/repositories          # Get user repositories
GET /github/commits               # Get recent commits
GET /github/issues                # Get user issues
GET /github/pull-requests         # Get pull requests
GET /github/ai-summary            # Get AI-powered GitHub summary
```

### Teams Integration
```http
GET /teams/login                  # Teams OAuth login
GET /teams/callback               # Teams OAuth callback
GET /teams/status                 # Check Teams auth status
GET /teams/summary                # Get Teams summary
GET /teams/teams                  # Get user's teams
GET /teams/channels               # Get all channels
GET /teams/messages               # Get recent messages
GET /teams/meetings               # Get user's meetings
GET /teams/ai-summary             # Get AI-powered Teams summary
```

### Chatbot APIs
```http
POST /chatbot/chat                # Chat with email assistant
GET /chatbot/suggestions          # Get email chat suggestions
POST /github-chatbot/chat         # Chat with GitHub assistant
GET /github-chatbot/suggestions   # Get GitHub chat suggestions
POST /teams-chatbot/chat          # Chat with Teams assistant
GET /teams-chatbot/suggestions    # Get Teams chat suggestions
```

## 💬 Chatbot Examples

### Email Assistant
```
User: "How many unread emails do I have?"
Assistant: "You currently have 15 unread emails. The most recent ones are from..."

User: "Show me emails from john@example.com"
Assistant: "I found 3 emails from john@example.com. The most recent one is..."

User: "What are my most important emails?"
Assistant: "Based on your email patterns, here are the most important emails..."
```

### GitHub Assistant
```
User: "How many repositories do I have?"
Assistant: "You have 12 repositories. The most active ones are..."

User: "What are my recent commits?"
Assistant: "Your most recent commits include..."

User: "Show me my open issues"
Assistant: "You have 5 open issues across your repositories..."
```

### Teams Assistant
```
User: "How many teams do I have?"
Assistant: "You are a member of 8 teams. The most active ones are..."

User: "What meetings do I have today?"
Assistant: "You have 3 meetings scheduled for today..."

User: "Show me recent messages from my teams"
Assistant: "Recent activity in your teams includes..."
```

## 🏗️ Project Structure

```
_MCP_Agent/
├── api/
│   ├── main.py                    # FastAPI application entry point
│   ├── models/                    # Pydantic data models
│   │   ├── auth.py               # Authentication models
│   │   ├── chatbot.py            # Chatbot models
│   │   ├── github.py             # GitHub models
│   │   └── teams.py              # Teams models
│   ├── routers/                   # API route handlers
│   │   ├── auth.py               # Authentication routes
│   │   ├── emails.py             # Email management routes
│   │   ├── chatbot.py            # Email chatbot routes
│   │   ├── github.py             # GitHub routes
│   │   ├── github_chatbot.py     # GitHub chatbot routes
│   │   ├── teams.py              # Teams routes
│   │   └── teams_chatbot.py      # Teams chatbot routes
│   └── services/                  # Business logic services
│       ├── auth_service.py       # Microsoft authentication
│       ├── email_service.py      # Email operations
│       ├── ai_service.py         # AI summarization
│       ├── github_auth_service.py # GitHub authentication
│       ├── github_service.py     # GitHub operations
│       ├── github_chatbot_service.py # GitHub chatbot
│       ├── teams_auth_service.py # Teams authentication
│       ├── teams_service.py      # Teams operations
│       ├── teams_chatbot_service.py # Teams chatbot
│       └── chatbot_service.py    # Email chatbot
├── frontend/
│   └── templates/
│       └── dashboard.html        # Main dashboard template
├── app.py                        # Application launcher
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── GITHUB_SETUP.md              # GitHub setup guide
└── TEAMS_SETUP.md               # Teams setup guide
```

## 🔧 Configuration Options

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CLIENT_ID` | Microsoft Azure client ID | Yes | - |
| `CLIENT_SECRET` | Microsoft Azure client secret | Yes | - |
| `TENANT_ID` | Microsoft Azure tenant ID | Yes | - |
| `REDIRECT_URI` | OAuth redirect URI | No | `http://localhost:8000/auth/callback` |
| `SCOPES` | Microsoft Graph scopes | No | `Mail.Read User.Read` |
| `TEAMS_CLIENT_ID` | Teams client ID (same as CLIENT_ID) | Yes | - |
| `TEAMS_CLIENT_SECRET` | Teams client secret (same as CLIENT_SECRET) | Yes | - |
| `TEAMS_TENANT_ID` | Teams tenant ID (same as TENANT_ID) | Yes | - |
| `TEAMS_REDIRECT_URI` | Teams OAuth redirect URI | No | `http://localhost:8000/auth/teams/callback` |
| `TEAMS_SCOPES` | Teams scopes | No | `Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read` |
| `GITHUB_CLIENT_ID` | GitHub OAuth client ID | Yes | - |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth client secret | Yes | - |
| `GITHUB_REDIRECT_URI` | GitHub OAuth redirect URI | No | `http://localhost:8000/auth/github/callback` |
| `GITHUB_SCOPES` | GitHub scopes | No | `repo user` |
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes | - |

## 🚨 Troubleshooting

### Common Issues

#### 1. "Invalid client" Error
- Verify your Azure app registration is correct
- Check that CLIENT_ID and CLIENT_SECRET match your Azure app
- Ensure the app is registered as a web application

#### 2. "403 Forbidden" Errors
- Check that all required permissions are granted in Azure AD
- Verify admin consent is granted for all permissions
- Ensure the user has access to the requested resources

#### 3. "AADSTS50194" Error
- Make sure you're using a single-tenant app registration
- Verify TENANT_ID is set to your specific tenant ID
- Don't use "common" as the tenant ID

#### 4. "Field required: code" Error
- Check that redirect URIs match exactly
- Verify the OAuth flow is completing properly
- Ensure the app registration settings are correct

#### 5. AI Service Errors
- Verify GEMINI_API_KEY is set correctly
- Check that the Google Cloud project has Generative AI API enabled
- Ensure the API key has proper permissions

### Debug Mode

Add to your `.env` file for detailed logging:
```env
DEBUG=true
```

## 🔒 Security Considerations

### Production Deployment
1. **Use HTTPS**: Always use HTTPS in production
2. **Database Storage**: Replace in-memory token storage with a proper database
3. **Environment Variables**: Store sensitive data in environment variables
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Token Refresh**: Implement automatic token refresh logic
6. **Monitoring**: Add proper logging and monitoring

### Token Management
- Tokens are currently stored in memory (for development)
- Implement secure token storage for production
- Add token refresh logic for long-running sessions
- Implement proper token validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the browser console for JavaScript errors
2. Review the application logs for Python errors
3. Verify all environment variables are set correctly
4. Test with a different account if authentication issues persist
5. Check network connectivity to external APIs

## 🔄 Updates

Stay updated with the latest features and fixes:
```bash
git pull origin main
pip install -r requirements.txt
```

---

**Note**: This application is designed for development and testing purposes. For production use, implement proper security measures, database storage, and monitoring.