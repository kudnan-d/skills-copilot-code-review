"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from .backend import routers, database

# Initialize web host
app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database with sample data if empty
try:
    database.init_database()
except Exception as e:
    print(f"Warning: Database initialization error: {e}")
    # Continue running - database might not be needed immediately

# Mount the static files directory for serving the frontend
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Root endpoint to redirect to static index.html
@app.get("/")
def root():
    """Redirect to the main application page."""
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Include routers
app.include_router(routers.activities.router)
app.include_router(routers.auth.router)
