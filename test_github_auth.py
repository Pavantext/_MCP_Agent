#!/usr/bin/env python3
"""
Test script to check GitHub authentication
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_github_auth():
    """Test GitHub authentication endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing GitHub Authentication...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Server is running (status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running. Please start the server first.")
        return
    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
        return
    
    # Test 2: Check GitHub auth URL
    try:
        response = requests.get(f"{base_url}/auth/github")
        if response.status_code == 307:  # Redirect
            print("✓ GitHub auth redirect is working")
            print(f"  Redirect URL: {response.headers.get('location', 'Unknown')}")
        else:
            print(f"✗ GitHub auth redirect failed (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error testing GitHub auth: {e}")
    
    # Test 3: Check environment variables
    github_client_id = os.getenv('GITHUB_CLIENT_ID')
    github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    
    if github_client_id:
        print(f"✓ GitHub Client ID is set: {github_client_id[:10]}...")
    else:
        print("✗ GitHub Client ID is not set")
    
    if github_client_secret:
        print(f"✓ GitHub Client Secret is set: {github_client_secret[:10]}...")
    else:
        print("✗ GitHub Client Secret is not set")
    
    # Test 4: Check GitHub test endpoint
    try:
        response = requests.get(f"{base_url}/github/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ GitHub test endpoint working: {data}")
        else:
            print(f"✗ GitHub test endpoint failed (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error testing GitHub endpoint: {e}")
    
    print("\n" + "=" * 50)
    print("To test GitHub authentication:")
    print("1. Make sure GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET are set")
    print("2. Visit: http://localhost:8000/auth/github")
    print("3. Complete the OAuth flow")
    print("4. Check: http://localhost:8000/github/test")

if __name__ == "__main__":
    test_github_auth() 