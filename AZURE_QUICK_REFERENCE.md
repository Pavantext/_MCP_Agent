# Azure Credentials - Quick Reference

## 🎯 **Get These 3 Values from Azure**

### **1. CLIENT_ID**
- **Go to**: Azure Portal → App Registrations → Your App → Overview
- **Copy**: "Application (client) ID"
- **Format**: `12345678-1234-1234-1234-123456789012`

### **2. TENANT_ID**
- **For Multi-Tenant**: Always use `common`
- **Don't use**: The "Directory (tenant) ID" shown in portal

### **3. CLIENT_SECRET**
- **Go to**: App Registration → Certificates & secrets
- **Click**: "New client secret"
- **Copy**: The "Value" (not the ID)
- **Important**: Copy immediately - shown only once!

## 🔧 **Your .env File Should Look Like:**

```env
CLIENT_ID=12345678-1234-1234-1234-123456789012
CLIENT_SECRET=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
TENANT_ID=common
```

## 🚨 **Critical Settings in Azure:**

1. **Supported account types**: "Accounts in any organizational directory and personal Microsoft accounts"
2. **API Permissions**: Add all 8 Microsoft Graph permissions
3. **Grant admin consent**: Click "Grant admin consent"
4. **Redirect URIs**: Add your callback URLs

## ✅ **Test Your Setup:**

```bash
python deploy.py
```

If it shows "✅ All required environment variables are set", you're ready! 