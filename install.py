#!/usr/bin/env python3
"""
Installation script for MCP Multi-Service Dashboard API
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return True
    
    if os.path.exists('env_template.txt'):
        print("📝 Creating .env file from template...")
        try:
            with open('env_template.txt', 'r') as template:
                content = template.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(content)
            
            print("✅ .env file created successfully")
            print("⚠️  Please edit .env file with your actual API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("⚠️  env_template.txt not found, creating basic .env file...")
        try:
            with open('.env', 'w') as env_file:
                env_file.write("""# Microsoft OAuth Configuration (for Outlook Email)
MICROSOFT_CLIENT_ID=your_microsoft_client_id_here
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret_here

# GitHub OAuth Configuration (for GitHub Integration)
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Custom redirect URIs (defaults to localhost:8000)
MICROSOFT_REDIRECT_URI=http://localhost:8000/auth/callback
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
""")
            print("✅ Basic .env file created")
            print("⚠️  Please edit .env file with your actual API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False

def main():
    """Main installation function"""
    print("🚀 Installing MCP Multi-Service Dashboard API...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return 1
    
    print()
    
    # Create .env file
    create_env_file()
    
    print()
    print("✅ Installation completed!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python start.py")
    print("3. Visit http://localhost:8000")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 