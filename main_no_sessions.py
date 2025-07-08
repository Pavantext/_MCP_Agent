from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import routers after path setup
try:
    from api.routers import email_router, chatbot_router, auth_router, github_router
    from api.auth import is_authenticated
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required packages are installed:")
    print("pip install fastapi uvicorn python-multipart requests python-dotenv jinja2 aiofiles google-generativeai")
    sys.exit(1)

app = FastAPI(title="MCP Multi-Service Dashboard API", version="2.0.0")

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router)
app.include_router(email_router)
app.include_router(chatbot_router)
app.include_router(github_router)

@app.get("/")
async def root(request: Request):
    """Root endpoint - redirect to auth page"""
    return RedirectResponse(url="/auth")

@app.get("/dashboard")
async def dashboard_redirect(request: Request):
    """Redirect to auth page"""
    return RedirectResponse(url="/auth")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "MCP Dashboard API is running"}

if __name__ == "__main__":
    import uvicorn
    try:
        print("Starting MCP Multi-Service Dashboard API...")
        print("Visit http://localhost:8000 to access the application")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Please check your environment and dependencies") 