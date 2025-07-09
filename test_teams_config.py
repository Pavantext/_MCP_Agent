#!/usr/bin/env python3
"""
Test script to debug Teams configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_teams_config():
    """Test Teams configuration"""
    print("=== Teams Configuration Test ===")
    
    # Check required environment variables
    required_vars = [
        "TEAMS_CLIENT_ID",
        "TEAMS_CLIENT_SECRET", 
        "TEAMS_TENANT_ID",
        "TEAMS_REDIRECT_URI",
        "TEAMS_SCOPES"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Mask sensitive values
            if "SECRET" in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease add these to your .env file:")
        for var in missing_vars:
            if var == "TEAMS_CLIENT_ID":
                print(f"{var}=your_client_id_here")
            elif var == "TEAMS_CLIENT_SECRET":
                print(f"{var}=your_client_secret_here")
            elif var == "TEAMS_TENANT_ID":
                print(f"{var}=your_tenant_id_here")
            elif var == "TEAMS_REDIRECT_URI":
                print(f"{var}=http://localhost:8000/auth/teams/callback")
            elif var == "TEAMS_SCOPES":
                print(f"{var}=Chat.Read Chat.ReadWrite Channel.ReadBasic.All Team.ReadBasic.All User.Read")
    else:
        print("\n✅ All required Teams environment variables are set!")
    
    # Test auth URL generation
    try:
        from api.services.teams_auth_service import TeamsAuthService
        auth_service = TeamsAuthService()
        auth_url = auth_service.get_authorization_url()
        print(f"\n✅ Auth URL generated successfully:")
        print(f"URL: {auth_url}")
    except Exception as e:
        print(f"\n❌ Error generating auth URL: {str(e)}")
    
    print("\n=== Configuration Test Complete ===")

if __name__ == "__main__":
    test_teams_config() 