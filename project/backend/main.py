import sys
import os
from pathlib import Path

# Add the app directory to the path so imports work correctly
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize database
from models.database import init_db, seed_initial_data

# Import routes
from routes.auth_routes import router as auth_router
from routes.employee_routes import router as employee_router
from routes.dashboard_routes import router as dashboard_router

# Initialize FastAPI app
app = FastAPI(
    title="New-Hire Onboarding Concierge",
    description="AI-powered employee onboarding orchestration system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(dashboard_router)

# Mount static files from frontend directory
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    seed_initial_data()
    print("Database initialized with seed data")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Onboarding Concierge API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
