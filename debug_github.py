#!/usr/bin/env python3
"""
Debug script to test GitHub service directly
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.services.github_service import GitHubService

# Load environment variables
load_dotenv()

def test_github_service():
    """Test GitHub service directly"""
    print("Testing GitHub Service...")
    print("=" * 50)
    
    # Check environment variables
    github_client_id = os.getenv('GITHUB_CLIENT_ID')
    github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    
    print(f"GitHub Client ID: {'Set' if github_client_id else 'Not set'}")
    print(f"GitHub Client Secret: {'Set' if github_client_secret else 'Not set'}")
    
    # Test with a sample token (this won't work but will show the structure)
    service = GitHubService()
    
    # Test the service methods with a dummy token
    dummy_token = "dummy_token_for_testing"
    
    print("\nTesting service methods with dummy token:")
    
    try:
        user_info = service.get_user_info(dummy_token)
        print(f"get_user_info result: {type(user_info)}")
    except Exception as e:
        print(f"get_user_info error: {e}")
    
    try:
        repos = service.get_repositories(dummy_token)
        print(f"get_repositories result: {type(repos)}")
    except Exception as e:
        print(f"get_repositories error: {e}")
    
    try:
        issues = service.get_issues(dummy_token)
        print(f"get_issues result: {type(issues)}")
    except Exception as e:
        print(f"get_issues error: {e}")
    
    try:
        prs = service.get_pull_requests(dummy_token)
        print(f"get_pull_requests result: {type(prs)}")
    except Exception as e:
        print(f"get_pull_requests error: {e}")
    
    try:
        activity = service.get_activity(dummy_token)
        print(f"get_activity result: {type(activity)}")
    except Exception as e:
        print(f"get_activity error: {e}")
    
    print("\n" + "=" * 50)
    print("Service structure looks good!")
    print("The errors above are expected with a dummy token.")
    print("Real authentication will be needed for actual API calls.")

if __name__ == "__main__":
    test_github_service() 