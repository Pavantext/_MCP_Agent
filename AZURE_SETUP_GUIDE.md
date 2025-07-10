# Azure Multi-Tenant App Setup Guide

## 🎯 **Step-by-Step Guide to Get Azure Credentials**

### **Step 1: Access Azure Portal**

1. **Go to Azure Portal**
   - Visit: https://portal.azure.com
   - Sign in with your Microsoft account

2. **Navigate to Azure Active Directory**
   - Click on the search bar at the top
   - Type "Azure Active Directory"
   - Click on "Azure Active Directory" from the results

### **Step 2: Create App Registration**

1. **Go to App Registrations**
   - In the left sidebar, click on "App registrations"
   - Click "New registration" button

2. **Fill in App Details**
   ```
   Name: MCP Agent Dashboard
   Supported account types: Accounts in any organizational directory and personal Microsoft accounts
   Redirect URI: Web - https://yourdomain.com/auth/callback
   ```
   
   **Important Notes:**
   - **Name**: Choose any name you like
   - **Supported account types**: Select "Accounts in any organizational directory and personal Microsoft accounts" (this makes it multi-tenant)
   - **Redirect URI**: For development, use `http://localhost:8000/auth/callback`. For production, use `https://yourdomain.com/auth/callback`

3. **Click "Register"**
   - Wait for the app to be created
   - You'll be redirected to the app overview page

### **Step 3: Get CLIENT_ID**

1. **Copy the Application (client) ID**
   - On the app overview page, you'll see "Application (client) ID"
   - This is your `CLIENT_ID`
   - Copy this value (it looks like: `12345678-1234-1234-1234-123456789012`)

### **Step 4: Get TENANT_ID**

1. **Copy the Directory (tenant) ID**
   - On the same overview page, you'll see "Directory (tenant) ID"
   - **For multi-tenant apps, use `common` instead**
   - So your `TENANT_ID=common`

### **Step 5: Create CLIENT_SECRET**

1. **Go to Certificates & secrets**
   - In the left sidebar, click "Certificates & secrets"

2. **Create New Client Secret**
   - Click "New client secret"
   - Add a description (e.g., "Production Secret")
   - Choose expiration (recommend 12 months or 24 months)
   - Click "Add"

3. **Copy the Secret Value**
   - **IMPORTANT**: Copy the "Value" immediately (not the ID)
   - The secret will only be shown once
   - This is your `CLIENT_SECRET`

### **Step 6: Configure API Permissions**

1. **Go to API permissions**
   - In the left sidebar, click "API permissions"

2. **Add Microsoft Graph Permissions**
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Choose "Delegated permissions"
   - Search and add these permissions:
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

3. **Grant Admin Consent**
   - Click "Grant admin consent for [Your Organization]"
   - Click "Yes" to confirm

### **Step 7: Configure Redirect URIs**

1. **Go to Authentication**
   - In the left sidebar, click "Authentication"

2. **Add Redirect URIs**
   - Under "Platform configurations", click "Add a platform"
   - Choose "Web"
   - Add these redirect URIs:
     ```
     http://localhost:8000/auth/callback
     http://localhost:8000/auth/teams/callback
     https://yourdomain.com/auth/callback
     https://yourdomain.com/auth/teams/callback
     ```

3. **Save Configuration**
   - Click "Configure"
   - Click "Save"

## 🔑 **Your Environment Variables**

After completing the setup, your environment variables should look like this:

```env
# Azure Multi-Tenant Configuration
CLIENT_ID=12345678-1234-1234-1234-123456789012
CLIENT_SECRET=your_secret_value_here
TENANT_ID=common
REDIRECT_URI=https://yourdomain.com/auth/callback
SCOPES=Mail.Read User.Read Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All Calendars.Read OnlineMeetings.Read

# Teams Configuration (uses same app)
TEAMS_CLIENT_ID=12345678-1234-1234-1234-123456789012
TEAMS_CLIENT_SECRET=your_secret_value_here
TEAMS_TENANT_ID=common
TEAMS_REDIRECT_URI=https://yourdomain.com/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read
```

## 🚨 **Important Security Notes**

### **Client Secret Security**
- **Never commit secrets to version control**
- **Store secrets securely** (environment variables, Azure Key Vault, etc.)
- **Rotate secrets regularly** (every 12-24 months)
- **Use different secrets for development and production**

### **Redirect URI Security**
- **Use HTTPS for production**
- **Never use HTTP in production**
- **Validate redirect URIs** to prevent attacks

## 🔍 **Troubleshooting**

### **Common Issues**

1. **"Application is not configured as multi-tenant"**
   - Solution: Make sure you selected "Accounts in any organizational directory and personal Microsoft accounts"

2. **"Client is public so neither 'client_assertion' nor 'client_secret' should be presented"**
   - Solution: Make sure "Allow public client flows" is **disabled** in Authentication settings

3. **"Invalid redirect URI"**
   - Solution: Add the exact redirect URI to the app registration

4. **"Insufficient privileges"**
   - Solution: Grant admin consent for all permissions

### **Verification Steps**

1. **Test the app registration**
   ```bash
   python deploy.py
   ```

2. **Check environment variables**
   ```bash
   echo $CLIENT_ID
   echo $TENANT_ID
   ```

3. **Test authentication flow**
   - Start your application
   - Try to login
   - Check logs for any errors

## 📋 **Checklist**

- [ ] Created multi-tenant app registration
- [ ] Copied Application (client) ID
- [ ] Set TENANT_ID=common
- [ ] Created and copied client secret
- [ ] Added all required API permissions
- [ ] Granted admin consent
- [ ] Configured redirect URIs
- [ ] Updated environment variables
- [ ] Tested authentication flow

## 🎯 **Next Steps**

After getting your Azure credentials:

1. **Set up GitHub OAuth app** (see GitHub setup guide)
2. **Configure Google Cloud** (for AI features)
3. **Update your .env file** with all credentials
4. **Deploy with HTTPS** (required for production)
5. **Test with different account types**

This multi-tenant setup will allow any user with a Microsoft account to login to your application without any technical setup! 