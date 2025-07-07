#!/usr/bin/env python3
"""
MCP Outlook Reader - Main Application Entry Point
A modular API service for reading and summarizing Outlook emails
"""

import uvicorn
from api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 