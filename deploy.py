#!/usr/bin/env python3
"""
Deployment script for MCP Agent Dashboard
Helps configure multi-tenant authentication for production deployment
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        "CLIENT_ID",
        "CLIENT_SECRET", 
        "GITHUB_CLIENT_ID",
        "GITHUB_CLIENT_SECRET",
        "GEMINI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def create_env_template():
    """Create a template .env file for production"""
    template = """# Production Environment Variables
# Replace these values with your actual credentials

# Microsoft Azure Multi-Tenant App (Email & Teams)
CLIENT_ID=your_multi_tenant_client_id_here
CLIENT_SECRET=your_multi_tenant_client_secret_here
TENANT_ID=common
REDIRECT_URI=https://yourdomain.com/auth/callback
SCOPES=Mail.Read User.Read Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All Calendars.Read OnlineMeetings.Read

# Teams Configuration (uses same app as above)
TEAMS_CLIENT_ID=your_multi_tenant_client_id_here
TEAMS_CLIENT_SECRET=your_multi_tenant_client_secret_here
TEAMS_TENANT_ID=common
TEAMS_REDIRECT_URI=https://yourdomain.com/auth/teams/callback
TEAMS_SCOPES=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read Calendars.Read OnlineMeetings.Read

# GitHub OAuth App
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/github/callback
GITHUB_SCOPES=repo user

# Google Cloud Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Debug mode
DEBUG=false
"""
    
    with open(".env.production", "w") as f:
        f.write(template)
    
    print("✅ Created .env.production template")
    print("📝 Update the values with your actual credentials")

def print_setup_instructions():
    """Print setup instructions for multi-tenant deployment"""
    print("\n" + "="*60)
    print("🚀 MULTI-TENANT DEPLOYMENT SETUP")
    print("="*60)
    
    print("\n📋 Step 1: Create Multi-Tenant Azure App")
    print("1. Go to Azure Portal → Azure Active Directory → App registrations")
    print("2. Click 'New registration'")
    print("3. Configure:")
    print("   - Name: MCP Agent Dashboard")
    print("   - Supported account types: Accounts in any organizational directory and personal Microsoft accounts")
    print("   - Redirect URI: Web - https://yourdomain.com/auth/callback")
    print("4. Add API Permissions (Microsoft Graph → Delegated):")
    print("   - Mail.Read")
    print("   - User.Read") 
    print("   - Chat.Read")
    print("   - Chat.ReadWrite")
    print("   - Channel.ReadBasic.All")
    print("   - Team.ReadBasic.All")
    print("   - Calendars.Read")
    print("   - OnlineMeetings.Read")
    print("5. Grant admin consent")
    
    print("\n📋 Step 2: Create GitHub OAuth App")
    print("1. Go to GitHub Settings → Developer settings → OAuth Apps")
    print("2. Click 'New OAuth App'")
    print("3. Configure:")
    print("   - Application name: MCP Agent Dashboard")
    print("   - Homepage URL: https://yourdomain.com")
    print("   - Authorization callback URL: https://yourdomain.com/auth/github/callback")
    
    print("\n📋 Step 3: Set up Google Cloud")
    print("1. Go to Google Cloud Console")
    print("2. Create new project or select existing")
    print("3. Enable Generative AI API")
    print("4. Create API key")
    
    print("\n📋 Step 4: Update Environment Variables")
    print("1. Copy values from your app registrations")
    print("2. Update .env.production with your credentials")
    print("3. Deploy with HTTPS")
    
    print("\n✅ Benefits of Multi-Tenant Setup:")
    print("- Users just click 'Login' - no setup required")
    print("- Works with any Microsoft account (personal or organizational)")
    print("- Single app handles all users")
    print("- Automatic permission handling")

def check_https_requirements():
    """Check if HTTPS is configured for production"""
    print("\n🔒 HTTPS Requirements:")
    print("- Azure requires HTTPS for production redirect URIs")
    print("- GitHub requires HTTPS for OAuth callbacks")
    print("- Use SSL certificates for your domain")
    print("- Update all redirect URIs to use https://")

def main():
    """Main deployment script"""
    print("🚀 MCP Agent Dashboard - Deployment Setup")
    print("="*50)
    
    # Check current environment
    if not check_environment():
        print("\n💡 Run this script to set up production deployment")
        create_env_template()
        print_setup_instructions()
        check_https_requirements()
        return
    
    # If environment is set, show deployment status
    print("\n✅ Environment is configured!")
    print("🚀 Ready for deployment")
    
    print("\n📋 Next Steps:")
    print("1. Deploy to your hosting platform")
    print("2. Configure HTTPS")
    print("3. Set up database for token storage")
    print("4. Test with different account types")

if __name__ == "__main__":
    main() 