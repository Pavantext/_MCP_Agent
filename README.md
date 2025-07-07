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

## 📡 API Endpoints

### Authentication
- `GET /auth/login` - Redirect to Microsoft OAuth
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/status` - Check authentication status
- `POST /auth/logout` - Logout user
- `GET /auth/token` - Get access token

### Emails
- `GET /emails/summary` - Get basic email summary
- `GET /emails/unread` - Get unread emails list
- `GET /emails/ai-summary` - Get AI-powered summary
- `PATCH /emails/{email_id}/read` - Mark email as read

### Web Interface
- `GET /` - Main entry point (redirects based on auth)
- `GET /dashboard` - Email summary dashboard
- `GET /docs` - API documentation (Swagger UI)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLIENT_ID` | Azure App Registration Client ID | Yes |
| `TENANT_ID` | Azure Directory (Tenant) ID | Yes |
| `REDIRECT_URI` | OAuth redirect URI | Yes |
| `SCOPES` | Microsoft Graph API scopes | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

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