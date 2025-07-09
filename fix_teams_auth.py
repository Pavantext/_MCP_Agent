#!/usr/bin/env python3
"""
Fix script for Teams authentication issues
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_teams_auth():
    """Check Teams authentication status"""
    print("=== Teams Authentication Check ===")
    
    # Check if we can reach the Teams login endpoint
    try:
        response = requests.get("http://localhost:8000/teams/login")
        if response.status_code == 200:
            print("✅ Teams login endpoint is accessible")
            data = response.json()
            if "auth_url" in data:
                print(f"✅ Auth URL generated: {data['auth_url']}")
                
                # Check if the auth URL uses the correct tenant
                tenant_id = os.getenv("TEAMS_TENANT_ID")
                if tenant_id and tenant_id != "common" and f"/{tenant_id}/" in data["auth_url"]:
                    print("✅ Auth URL uses correct tenant ID")
                else:
                    print("❌ Auth URL may be using incorrect tenant ID")
            else:
                print("❌ No auth URL in response")
        else:
            print(f"❌ Teams login endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach Teams login endpoint: {str(e)}")
    
    # Check environment variables
    print("\n=== Environment Variables ===")
    tenant_id = os.getenv("TEAMS_TENANT_ID")
    client_id = os.getenv("TEAMS_CLIENT_ID")
    
    if tenant_id and tenant_id != "common":
        print(f"✅ TEAMS_TENANT_ID is set to: {tenant_id}")
    else:
        print("❌ TEAMS_TENANT_ID is not set or is 'common'")
        print("   Please set it to your specific tenant ID")
    
    if client_id:
        print(f"✅ TEAMS_CLIENT_ID is set to: {client_id}")
    else:
        print("❌ TEAMS_CLIENT_ID is not set")
    
    print("\n=== Troubleshooting Steps ===")
    print("1. Make sure your Azure AD app is registered as 'Single tenant'")
    print("2. Verify TEAMS_TENANT_ID is set to your specific tenant ID (not 'common')")
    print("3. Check that the redirect URI in Azure AD matches exactly:")
    print("   http://localhost:8000/auth/teams/callback")
    print("4. Ensure all required API permissions are granted")
    print("5. Try creating a new app registration if the current one is multi-tenant")

if __name__ == "__main__":
    check_teams_auth() 