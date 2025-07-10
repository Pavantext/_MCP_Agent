# Azure Multi-Tenant Setup - Visual Guide

## 🎯 **Quick Reference: Where to Find Your Credentials**

### **CLIENT_ID (Application ID)**
**Location**: App Registration → Overview
**What to look for**: "Application (client) ID"
**Format**: `12345678-1234-1234-1234-123456789012`

### **TENANT_ID**
**For Multi-Tenant**: Always use `common`
**Don't use**: The "Directory (tenant) ID" shown in the portal

### **CLIENT_SECRET**
**Location**: App Registration → Certificates & secrets
**What to look for**: "Value" column (not the ID)
**Important**: Copy immediately - it's only shown once!

## 📋 **Step-by-Step Visual Guide**

### **Step 1: Create App Registration**

1. **Go to Azure Portal**: https://portal.azure.com
2. **Search for "Azure Active Directory"**
3. **Click "App registrations"**
4. **Click "New registration"**

**Fill in these details:**
```
Name: MCP Agent Dashboard
Supported account types: Accounts in any organizational directory and personal Microsoft accounts
Redirect URI: Web - http://localhost:8000/auth/callback
```

**Important**: The "Supported account types" setting makes it multi-tenant!

### **Step 2: Get CLIENT_ID**

After registration, you'll see the Overview page:

```
┌─────────────────────────────────────┐
│ Application (client) ID             │ ← Copy this
│ 12345678-1234-1234-1234-123456789012│
│                                     │
│ Directory (tenant) ID               │ ← Don't use this
│ 87654321-4321-4321-4321-210987654321│
└─────────────────────────────────────┘
```

**Copy the "Application (client) ID"** - this is your `CLIENT_ID`

### **Step 3: Create CLIENT_SECRET**

1. **Click "Certificates & secrets"** in the left menu
2. **Click "New client secret"**
3. **Add description**: "Production Secret"
4. **Choose expiration**: 12 months
5. **Click "Add"**

**IMPORTANT**: Copy the "Value" immediately:
```
┌─────────────────────────────────────┐
│ ID        │ Description │ Expires   │
│ Secret 1  │ Production  │ 2025-01-01│
│           │ Secret      │           │
│           │             │           │
│ VALUE:    │ ← Copy this │           │
│ abc123... │             │           │
└─────────────────────────────────────┘
```

### **Step 4: Configure Permissions**

1. **Click "API permissions"** in the left menu
2. **Click "Add a permission"**
3. **Select "Microsoft Graph"**
4. **Choose "Delegated permissions"**
5. **Search and add these permissions**:

```
✅ Mail.Read
✅ User.Read
✅ Chat.Read
✅ Chat.ReadWrite
✅ Channel.ReadBasic.All
✅ Team.ReadBasic.All
✅ Calendars.Read
✅ OnlineMeetings.Read
```

6. **Click "Grant admin consent"**

### **Step 5: Configure Redirect URIs**

1. **Click "Authentication"** in the left menu
2. **Click "Add a platform"**
3. **Choose "Web"**
4. **Add these redirect URIs**:

```
http://localhost:8000/auth/callback
http://localhost:8000/auth/teams/callback
https://yourdomain.com/auth/callback
https://yourdomain.com/auth/teams/callback
```

5. **Click "Configure"**
6. **Click "Save"**

## 🔑 **Your Final Environment Variables**

```env
# Azure Multi-Tenant Configuration
CLIENT_ID=12345678-1234-1234-1234-123456789012
CLIENT_SECRET=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
TENANT_ID=common
REDIRECT_URI=http://localhost:8000/auth/callback
SCOPES=Mail.Read User.Read Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All Calendars.Read OnlineMeetings.Read

# Teams Configuration (uses same app)
TEAMS_CLIENT_ID=12345678-1234-1234-1234-123456789012
TEAMS_CLIENT_SECRET=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
TEAMS_TENANT_ID=common
TEAMS_REDIRECT_URI=http://localhost:8000/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read
```

## 🚨 **Common Mistakes to Avoid**

### **❌ Don't Do This:**
- Use the "Directory (tenant) ID" for TENANT_ID
- Copy the secret ID instead of the value
- Forget to grant admin consent
- Use HTTP redirect URIs in production
- Commit secrets to version control

### **✅ Do This:**
- Use `TENANT_ID=common` for multi-tenant
- Copy the secret "Value" immediately
- Grant admin consent for all permissions
- Use HTTPS redirect URIs for production
- Store secrets securely

## 🔍 **Verification Checklist**

After setup, verify:

- [ ] App registration shows "Multi-tenant" under "Supported account types"
- [ ] All 8 permissions are listed under "API permissions"
- [ ] Admin consent shows "Granted for [Your Organization]"
- [ ] Redirect URIs are configured correctly
- [ ] Client secret is copied (not the ID)
- [ ] Environment variables are set correctly

## 🎯 **Test Your Setup**

1. **Run the deployment script**:
   ```bash
   python deploy.py
   ```

2. **Start your application**:
   ```bash
   python app.py
   ```

3. **Try to login** at http://localhost:8000

4. **Check for any errors** in the console

If everything works, you'll see the login page and be able to authenticate with any Microsoft account! 