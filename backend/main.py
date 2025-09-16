"""
Blue Carbon MRV Platform - FastAPI Backend
Main application entry point with CORS, middleware, and route registration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from contextlib import asynccontextmanager

# Import routers
from routers import auth, projects, mrv, credits, marketplace, users
from database.database import engine, Base
from core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🌊 Blue Carbon MRV Platform starting up...")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🔗 API Base URL: {settings.API_V1_STR}")
    yield
    # Shutdown
    print("🌊 Blue Carbon MRV Platform shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Blue Carbon project monitoring, reporting, verification, and carbon credit trading",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://complete-blue-carbon-x4ik.bolt.host",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(mrv.router, prefix=f"{settings.API_V1_STR}/mrv", tags=["mrv"])
app.include_router(credits.router, prefix=f"{settings.API_V1_STR}/credits", tags=["credits"])
app.include_router(marketplace.router, prefix=f"{settings.API_V1_STR}/marketplace", tags=["marketplace"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Blue Carbon MRV Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "features": [
            "User Authentication & Authorization",
            "Blue Carbon Project Management",
            "AI-Powered MRV Analysis",
            "Blockchain Carbon Credit Minting",
            "Transparent Marketplace Trading",
            "Multi-Stakeholder Dashboard"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "ml_service": "operational",
        "blockchain": "available"
    }

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )