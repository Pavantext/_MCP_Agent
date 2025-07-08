#!/usr/bin/env python3
"""
Setup script to help configure environment variables
"""

import os
from pathlib import Path

def setup_env():
    """Setup environment variables"""
    print("Setting up environment variables...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            print("Current .env content:")
            print("-" * 30)
            print(content)
            print("-" * 30)
    else:
        print("✗ .env file not found")
        
        # Check if env_template.txt exists
        template_file = Path("env_template.txt")
        if template_file.exists():
            print("✓ Found env_template.txt")
            
            # Copy template to .env
            with open(template_file, 'r') as f:
                template_content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(template_content)
            
            print("✓ Created .env file from template")
            print("Please edit .env file with your actual credentials")
        else:
            print("✗ No template file found")
            return
    
    print("\n" + "=" * 50)
    print("To get GitHub credentials:")
    print("1. Go to https://github.com/settings/developers")
    print("2. Click 'New OAuth App'")
    print("3. Set Application name: 'MCP Agent'")
    print("4. Set Homepage URL: 'http://localhost:8000'")
    print("5. Set Authorization callback URL: 'http://localhost:8000/auth/github/callback'")
    print("6. Copy the Client ID and Client Secret")
    print("7. Edit .env file and replace the placeholder values")
    print("\nExample .env content:")
    print("GITHUB_CLIENT_ID=your_actual_client_id_here")
    print("GITHUB_CLIENT_SECRET=your_actual_client_secret_here")
    
    # Test current environment
    print("\n" + "=" * 50)
    print("Testing current environment:")
    
    github_client_id = os.getenv('GITHUB_CLIENT_ID')
    github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
    
    if github_client_id and github_client_id != "your_github_client_id_here":
        print(f"✓ GitHub Client ID is set: {github_client_id[:10]}...")
    else:
        print("✗ GitHub Client ID is not set or is placeholder")
    
    if github_client_secret and github_client_secret != "your_github_client_secret_here":
        print(f"✓ GitHub Client Secret is set: {github_client_secret[:10]}...")
    else:
        print("✗ GitHub Client Secret is not set or is placeholder")

if __name__ == "__main__":
    setup_env() 