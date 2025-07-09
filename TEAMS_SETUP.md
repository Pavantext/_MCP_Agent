# Microsoft Teams Integration Setup

This guide will help you set up Microsoft Teams integration for the MCP Agent application.

## Prerequisites

1. A Microsoft Azure account
2. Access to Azure Active Directory (Azure AD)
3. Python 3.8+ installed
4. The application running locally

## Step 1: Register Application in Azure AD

1. Go to the [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: MCP Teams Agent
   - **Supported account types**: Accounts in this organizational directory only (Single tenant)
   - **Redirect URI**: Web - `http://localhost:8000/auth/teams/callback`
5. Click **Register**
6. **Important**: Copy your **Directory (tenant) ID** from the Overview page

**⚠️ CRITICAL**: Make sure you select "Accounts in this organizational directory only" (Single tenant). Do NOT select "Accounts in any organizational directory" as this will cause the AADSTS50194 error.

### If You Already Have an App Registration

If you already have an app registration that's causing the AADSTS50194 error:

1. Go to your app registration in Azure AD
2. Click on **Authentication** in the left menu
3. Under **Platform configurations**, find your Web platform
4. Make sure the redirect URI is exactly: `http://localhost:8000/auth/teams/callback`
5. Go to **Overview** and check the **Supported account types**
6. If it shows "Accounts in any organizational directory", you need to create a new app registration with "Accounts in this organizational directory only"

**Note**: You cannot change the account types after registration, so you'll need to create a new app if the current one is multi-tenant.

## Step 2: Configure API Permissions

1. In your registered app, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add the following permissions:
   - `Chat.Read`
   - `Chat.ReadWrite`
   - `Channel.ReadBasic.All`
   - `Team.ReadBasic.All`
   - `User.Read`
   - `Calendars.Read`
   - `OnlineMeetings.Read`
6. Click **Add permissions**
7. Click **Grant admin consent** (if you have admin rights)

## Step 3: Get Client Credentials

1. In your registered app, go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and select expiration
4. Copy the **Value** (this is your client secret)
5. Go to **Overview** and copy the **Application (client) ID**
6. Copy the **Directory (tenant) ID** from the Overview page

## Step 4: Configure Environment Variables

Create or update your `.env` file with the following variables:

```env
# Teams Configuration
TEAMS_CLIENT_ID=your_client_id_here
TEAMS_CLIENT_SECRET=your_client_secret_here
TEAMS_TENANT_ID=your_tenant_id_here
TEAMS_REDIRECT_URI=http://localhost:8000/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read

# AI Configuration (if not already set)
GOOGLE_API_KEY=your_google_api_key_here
```

## Step 5: Test the Integration

1. Start the application:
   ```bash
   python app.py
   ```

2. Navigate to `http://localhost:8000`

3. Log in with your Microsoft account

4. Click the **"💬 Connect to Teams"** button

5. Complete the OAuth flow

6. You should see Teams summary and chatbot features appear

## API Endpoints

The Teams integration provides the following endpoints:

### Authentication
- `GET /teams/login` - Initiate Teams OAuth login
- `GET /teams/callback` - Handle OAuth callback
- `GET /teams/status` - Check authentication status
- `POST /teams/logout` - Logout from Teams

### Data Retrieval
- `GET /teams/summary` - Get Teams summary
- `GET /teams/teams` - Get user's teams
- `GET /teams/channels` - Get all channels
- `GET /teams/messages` - Get recent messages
- `GET /teams/meetings` - Get user's meetings
- `GET /teams/meetings/{meeting_id}` - Get meeting details
- `GET /teams/meetings/{meeting_id}/attendance` - Get meeting attendance
- `GET /teams/ai-summary` - Get AI-powered summary

### Chatbot
- `POST /teams-chatbot/chat` - Chat with Teams assistant
- `GET /teams-chatbot/suggestions` - Get chat suggestions

## Features

### Teams Summary
- Displays total teams, channels, messages, and meetings
- Shows AI-generated insights about Teams activity
- Highlights most active teams and channels
- Provides communication patterns analysis
- Includes meeting schedules and patterns

### Teams Assistant
- AI-powered chatbot for Teams data
- Answers questions about teams, channels, messages, and meetings
- Provides insights about collaboration patterns
- Suggests relevant questions
- Helps with meeting information and scheduling

## Troubleshooting

### Common Issues

1. **"Invalid client" error**
   - Check that your `TEAMS_CLIENT_ID` is correct
   - Verify the app registration in Azure AD

2. **"Invalid redirect URI" error**
   - Ensure the redirect URI in Azure AD matches your `.env` file
   - Check that `TEAMS_REDIRECT_URI` is set correctly

3. **"AADSTS50194: Application is not configured as multi-tenant" error**
   - Make sure you're using a single-tenant app registration
   - Set `TEAMS_TENANT_ID` to your specific tenant ID (not "common")
   - Verify the app is registered as "Accounts in this organizational directory only"

4. **"Insufficient permissions" error**
   - Verify all required permissions are granted in Azure AD
   - Check that admin consent is granted for the permissions

5. **"No data available"**
   - Ensure the user has access to Teams data
   - Check that the user is a member of teams with channels

6. **"Field required: code" error**
   - This usually means the OAuth flow was interrupted
   - Check that your redirect URI is exactly correct
   - Verify the app registration settings

### Debug Mode

To enable debug logging, add to your `.env` file:
```env
DEBUG=true
```

## Security Notes

- Store client secrets securely
- Use HTTPS in production
- Implement proper token storage (database instead of memory)
- Add rate limiting for API calls
- Consider implementing token refresh logic

## Production Deployment

For production deployment:

1. Update redirect URIs to your production domain
2. Use a proper database for token storage
3. Implement token refresh logic
4. Add proper error handling and logging
5. Use HTTPS for all communications
6. Implement rate limiting and monitoring

## Support

If you encounter issues:

1. Check the browser console for JavaScript errors
2. Review the application logs for Python errors
3. Verify Azure AD configuration
4. Test with a different Microsoft account
5. Check network connectivity to Microsoft Graph API 