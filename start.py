#!/usr/bin/env python3
"""
Startup script for MCP Multi-Service Dashboard API
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv',
        'jinja2',
        'aiofiles',
        'google-generativeai',
        'starlette'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✓ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            return False
    
    return True

def check_environment():
    """Check if environment file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("Please create a .env file with your API keys:")
        print("Copy from env_template.txt and fill in your values")
        return False
    print("✓ .env file found")
    return True

def check_project_structure():
    """Check if all required files exist"""
    required_files = [
        'api/__init__.py',
        'api/auth.py',
        'api/routers/__init__.py',
        'api/routers/auth_router.py',
        'api/routers/emails.py',
        'api/routers/chatbot.py',
        'api/routers/github_router.py',
        'api/services/email_service.py',
        'api/services/ai_service.py',
        'api/services/chatbot_service.py',
        'api/services/github_service.py',
        'api/models/auth.py',
        'api/models/chatbot.py',
        'api/models/github.py',
        'frontend/templates/dashboard.html',
        'frontend/templates/github_dashboard.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ {file_path} is missing")
        else:
            print(f"✓ {file_path} exists")
    
    if missing_files:
        print(f"\n❌ Missing files: {len(missing_files)}")
        return False
    
    return True

def test_session_middleware():
    """Test if session middleware is available"""
    try:
        from starlette.middleware.sessions import SessionMiddleware
        print("✓ Session middleware available")
        return True
    except ImportError:
        print("⚠️  Session middleware not available, using fallback mode")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting MCP Multi-Service Dashboard API...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    print()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    print()
    
    # Check environment
    if not check_environment():
        print("⚠️  Continuing without .env file (some features may not work)")
    
    print()
    
    # Check project structure
    if not check_project_structure():
        return 1
    
    print()
    
    # Test session middleware
    session_available = test_session_middleware()
    
    print()
    print("✅ All checks passed!")
    print("=" * 50)
    
    # Start the application
    try:
        print("🌐 Starting server...")
        print("📱 Visit http://localhost:8000 to access the application")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        if session_available:
            # Use main.py with session middleware
            from main import app
        else:
            # Use fallback without session middleware
            print("⚠️  Using fallback mode without session middleware")
            from main_no_sessions import app
        
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Try running: python main_no_sessions.py")
        print("2. Check if all dependencies are installed")
        print("3. Verify your .env file exists")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 