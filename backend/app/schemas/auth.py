"""
CampusMind AI - Auth Schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    enrollmentNumber: str
    department: str
    semester: str
    section: Optional[str] = "A"


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    enrollmentNumber: str
    department: str
    semester: str
    section: Optional[str] = "A"
    cgpa: Optional[float] = 8.5
    role: str = "student"
