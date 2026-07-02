"""
Authentication endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
from pydantic import BaseModel, Field

from ..database import teachers_collection, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


@router.post("/login")
def login(request: LoginRequest) -> Dict[str, Any]:
    """Login a teacher account - requires POST body with credentials.
    
    Args:
        request: LoginRequest containing username and password
        
    Returns:
        Teacher information with username, display_name, and role
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find the teacher in the database
    teacher = teachers_collection.find_one({"_id": request.username})

    # Verify password using Argon2 verifier from database.py
    if not teacher or not verify_password(teacher.get("password", ""), request.password):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    # Return teacher information (excluding password)
    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }


@router.get("/check-session")
def check_session(username: str) -> Dict[str, Any]:
    """Check if a session is valid by username.
    
    Args:
        username: Teacher username to validate
        
    Returns:
        Teacher information if valid
        
    Raises:
        HTTPException: If teacher not found
    """
    teacher = teachers_collection.find_one({"_id": username})

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }
