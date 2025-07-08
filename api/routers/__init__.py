# Routers module

from .emails import router as email_router
from .chatbot import router as chatbot_router
from .auth_router import router as auth_router
from .github_router import router as github_router

__all__ = [
    "email_router",
    "chatbot_router", 
    "auth_router",
    "github_router"
] 