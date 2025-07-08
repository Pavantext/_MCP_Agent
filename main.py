from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

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
    """Root endpoint - redirect to appropriate dashboard"""
    try:
        if is_authenticated(request):
            # Check which service is authenticated
            if request.session.get('access_token'):
                return RedirectResponse(url="/dashboard")
            elif request.session.get('github_access_token'):
                return RedirectResponse(url="/github/dashboard")
    except Exception as e:
        print(f"Error in root endpoint: {e}")
    
    return RedirectResponse(url="/auth")

@app.get("/dashboard")
async def dashboard_redirect(request: Request):
    """Redirect to appropriate dashboard based on authentication"""
    try:
        if not is_authenticated(request):
            return RedirectResponse(url="/auth")
        
        # Check which service is authenticated
        if request.session.get('access_token'):
            return RedirectResponse(url="/emails/dashboard")
        elif request.session.get('github_access_token'):
            return RedirectResponse(url="/github/dashboard")
        
        return RedirectResponse(url="/auth")
    except Exception as e:
        print(f"Error in dashboard redirect: {e}")
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