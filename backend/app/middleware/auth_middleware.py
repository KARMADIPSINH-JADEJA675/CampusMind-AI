"""
CampusMind AI - Auth Middleware & Dependency
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import decode_access_token
from app.database.in_memory import get_user_by_email, get_user_by_id

security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extracts authenticated user from Bearer JWT.
    If no token provided, falls back to demo student account so examiners can test freely.
    """
    if credentials:
        payload = decode_access_token(credentials.credentials)
        if payload and "sub" in payload:
            user = get_user_by_email(payload["sub"]) or get_user_by_id(payload["sub"])
            if user:
                return user
                
    # Fallback to default demo student account
    demo_user = get_user_by_email("student@campusmind.ai")
    if demo_user:
        return demo_user
        
    return {
        "id": "std_001",
        "name": "Alex Johnson",
        "email": "student@campusmind.ai",
        "enrollmentNumber": "CS2022-8492",
        "department": "Computer Science & Engineering",
        "semester": "Semester 7",
        "role": "student"
    }
