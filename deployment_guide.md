# Deployment Guide - User-Friendly Authentication

## 🎯 **Problem & Solution**

### **Current Problem:**
- Users need to create their own Azure app registrations
- Users need to configure API keys and secrets
- Complex setup process for each user
- Not scalable for deployment

### **Solution: Multi-Tenant Azure App**
- **One app registration** handles all users
- **Zero user setup** - just click login
- **Works for any Microsoft account** (personal or organizational)
- **Automatic permission handling**

## 🚀 **Implementation Options**

### **Option 1: Multi-Tenant Azure App (RECOMMENDED)**

#### **Step 1: Create Multi-Tenant Azure App Registration**

1. **Go to Azure Portal** → **Azure Active Directory** → **App registrations**
2. **Click "New registration"**
3. **Configure as follows:**
   ```
   Name: MCP Agent Dashboard
   Supported account types: Accounts in any organizational directory and personal Microsoft accounts
   Redirect URI: Web - https://yourdomain.com/auth/callback
   ```

4. **Add API Permissions:**
   - Microsoft Graph → Delegated permissions
   - Add ALL required permissions:
     ```
     Mail.Read
     User.Read
     Chat.Read
     Chat.ReadWrite
     Channel.ReadBasic.All
     Team.ReadBasic.All
     Calendars.Read
     OnlineMeetings.Read
     ```

5. **Grant admin consent** for all permissions

#### **Step 2: Update Environment Variables**

```env
# Single multi-tenant app for all users
CLIENT_ID=your_multi_tenant_client_id
CLIENT_SECRET=your_multi_tenant_client_secret
TENANT_ID=common
REDIRECT_URI=https://yourdomain.com/auth/callback
SCOPES=Mail.Read User.Read Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All Calendars.Read OnlineMeetings.Read

# Use same app for Teams
TEAMS_CLIENT_ID=your_multi_tenant_client_id
TEAMS_CLIENT_SECRET=your_multi_tenant_client_secret
TEAMS_TENANT_ID=common
TEAMS_REDIRECT_URI=https://yourdomain.com/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read

# GitHub (separate setup)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/github/callback
GITHUB_SCOPES=repo user

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key
```

#### **Step 3: Update Auth Services**

Update the auth services to use `common` tenant:

```python
# In api/services/auth_service.py
def __init__(self):
    self.client_id = os.getenv("CLIENT_ID")
    self.client_secret = os.getenv("CLIENT_SECRET")
    # Use 'common' for multi-tenant support
    self.tenant_id = os.getenv("TENANT_ID", "common")
    self.redirect_uri = os.getenv("REDIRECT_URI")
    self.scopes = os.getenv("SCOPES")
```

### **Option 2: GitHub OAuth App (For GitHub Integration)**

#### **Step 1: Create GitHub OAuth App**

1. **Go to GitHub Settings** → **Developer settings** → **OAuth Apps**
2. **Click "New OAuth App"**
3. **Configure:**
   ```
   Application name: MCP Agent Dashboard
   Homepage URL: https://yourdomain.com
   Authorization callback URL: https://yourdomain.com/auth/github/callback
   ```

#### **Step 2: Get GitHub Credentials**

1. Copy the **Client ID**
2. Generate a **Client Secret**
3. Add to environment variables

### **Option 3: Google Cloud Setup (For AI)**

#### **Step 1: Create Google Cloud Project**

1. **Go to Google Cloud Console**
2. **Create new project** or select existing
3. **Enable Generative AI API**

#### **Step 2: Get API Key**

1. **APIs & Services** → **Credentials**
2. **Create Credentials** → **API Key**
3. **Add to environment variables**

## 🔧 **Code Updates Required**

### **1. Update Auth Service for Multi-Tenant**

```python
# api/services/auth_service.py
def get_authorization_url(self) -> str:
    """Get Microsoft OAuth authorization URL"""
    base_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize"
    params = {
        "client_id": self.client_id,
        "response_type": "code",
        "redirect_uri": self.redirect_uri,
        "scope": self.scopes,
        "response_mode": "query"
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"
```

### **2. Update Teams Auth Service**

```python
# api/services/teams_auth_service.py
def __init__(self):
    self.client_id = os.getenv("TEAMS_CLIENT_ID")
    self.client_secret = os.getenv("TEAMS_CLIENT_SECRET")
    # Use 'common' for multi-tenant support
    self.tenant_id = os.getenv("TEAMS_TENANT_ID", "common")
    self.redirect_uri = os.getenv("TEAMS_REDIRECT_URI")
    self.scopes = os.getenv("TEAMS_SCOPES")
    self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
```

### **3. Add User Session Management**

```python
# api/models/auth.py
class UserSession(BaseModel):
    user_id: str
    email: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    github_token: Optional[str] = None
    teams_token: Optional[str] = None
```

## 🌐 **Deployment Considerations**

### **1. Domain Configuration**

Update all redirect URIs to your production domain:
```
https://yourdomain.com/auth/callback
https://yourdomain.com/auth/teams/callback
https://yourdomain.com/auth/github/callback
```

### **2. HTTPS Requirement**

- **Azure requires HTTPS** for production redirect URIs
- **GitHub requires HTTPS** for OAuth callbacks
- **Use SSL certificates** for your domain

### **3. Database for Token Storage**

Replace in-memory storage with database:

```python
# Example with SQLAlchemy
class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    email = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
    github_token = Column(String)
    teams_token = Column(String)
```

### **4. Environment Variables**

Set these in your production environment:

```bash
# Production environment variables
CLIENT_ID=your_multi_tenant_client_id
CLIENT_SECRET=your_multi_tenant_client_secret
TENANT_ID=common
REDIRECT_URI=https://yourdomain.com/auth/callback
SCOPES=Mail.Read User.Read Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All Calendars.Read OnlineMeetings.Read

TEAMS_CLIENT_ID=your_multi_tenant_client_id
TEAMS_CLIENT_SECRET=your_multi_tenant_client_secret
TEAMS_TENANT_ID=common
TEAMS_REDIRECT_URI=https://yourdomain.com/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/github/callback
GITHUB_SCOPES=repo user

GEMINI_API_KEY=your_gemini_api_key
```

## 🔒 **Security Best Practices**

### **1. Token Management**
- Store tokens securely in database
- Implement token refresh logic
- Add token expiration handling
- Encrypt sensitive data

### **2. Rate Limiting**
```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### **3. CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 **User Experience Flow**

### **For End Users:**

1. **Visit your application**
2. **Click "Login with Microsoft"**
3. **Grant permissions** (one-time)
4. **Access all features** (Email, Teams, GitHub)

### **For Organizations:**

1. **Admin sets up the multi-tenant app**
2. **Users just login** with their Microsoft accounts
3. **Automatic permission handling**
4. **Works with existing organizational accounts**

## 🚀 **Deployment Checklist**

- [ ] Create multi-tenant Azure app registration
- [ ] Configure all required permissions
- [ ] Set up GitHub OAuth app
- [ ] Configure Google Cloud for AI
- [ ] Update environment variables
- [ ] Deploy with HTTPS
- [ ] Set up database for token storage
- [ ] Configure CORS and security
- [ ] Test with different account types
- [ ] Monitor and log authentication

## 🎯 **Benefits of This Approach**

1. **Zero User Setup**: Users just click login
2. **Universal Compatibility**: Works with any Microsoft account
3. **Scalable**: One app handles all users
4. **Secure**: Proper token management
5. **User-Friendly**: No technical knowledge required
6. **Organizational Support**: Works with company accounts

This approach makes your application truly user-friendly and ready for production deployment!
