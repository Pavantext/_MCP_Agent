#!/usr/bin/env python3

try:
    print("Testing imports...")
    
    print("1. Testing FastAPI import...")
    from fastapi import FastAPI
    print("✓ FastAPI imported successfully")
    
    print("2. Testing router imports...")
    from api.routers import email_router, chatbot_router, auth_router, github_router
    print("✓ All routers imported successfully")
    
    print("3. Testing auth import...")
    from api.auth import get_current_user, is_authenticated
    print("✓ Auth functions imported successfully")
    
    print("4. Testing services...")
    from api.services.email_service import EmailService
    from api.services.ai_service import AIService
    print("✓ Services imported successfully")
    
    print("5. Testing models...")
    from api.models.auth import EmailSummary
    from api.models.chatbot import ChatMessage, ChatResponse
    print("✓ Models imported successfully")
    
    print("\n🎉 All imports successful! The application should work.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 