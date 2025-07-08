#!/usr/bin/env python3
"""
Test script to check GitHub auth URL generation
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.auth import get_github_auth_url

# Load environment variables
load_dotenv()

def test_github_auth_url():
    """Test GitHub auth URL generation"""
    print("Testing GitHub Auth URL Generation...")
    print("=" * 50)
    
    # Check environment variables
    github_client_id = os.getenv('GITHUB_CLIENT_ID')
    github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    
    print(f"GitHub Client ID: {'Set' if github_client_id else 'Not set'}")
    print(f"GitHub Client Secret: {'Set' if github_client_secret else 'Not set'}")
    
    if not github_client_id:
        print("✗ Cannot generate auth URL without GitHub Client ID")
        return
    
    # Generate auth URL
    try:
        auth_url = get_github_auth_url()
        print(f"✓ Generated auth URL: {auth_url}")
        
        # Check if URL looks correct
        if "github.com/login/oauth/authorize" in auth_url:
            print("✓ URL contains correct GitHub OAuth endpoint")
        else:
            print("✗ URL does not contain correct GitHub OAuth endpoint")
        
        if f"client_id={github_client_id}" in auth_url:
            print("✓ URL contains correct client ID")
        else:
            print("✗ URL does not contain correct client ID")
        
        if "scope=repo,user,read:org" in auth_url:
            print("✓ URL contains correct scopes")
        else:
            print("✗ URL does not contain correct scopes")
        
        if "redirect_uri=http://localhost:8000/auth/github/callback" in auth_url:
            print("✓ URL contains correct redirect URI")
        else:
            print("✗ URL does not contain correct redirect URI")
        
    except Exception as e:
        print(f"✗ Error generating auth URL: {e}")
    
    print("\n" + "=" * 50)
    print("If all checks pass, the auth URL should work correctly.")

if __name__ == "__main__":
    test_github_auth_url() 