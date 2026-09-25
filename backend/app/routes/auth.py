"""
CampusMind AI - Auth Routes
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserProfileResponse
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.database.in_memory import get_user_by_email, create_user
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegisterRequest):
    existing = get_user_by_email(payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
        
    hashed = hash_password(payload.password)
    user_id = f"std_{abs(hash(payload.email)) % 100000:04d}"
    
    new_user = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
        "password_hash": hashed,
        "plain_password_demo": payload.password,
        "enrollmentNumber": payload.enrollmentNumber,
        "department": payload.department,
        "semester": payload.semester,
        "section": payload.section or "A",
        "cgpa": 8.5,
        "role": "student"
    }
    
    create_user(new_user)
    token = create_access_token({"sub": new_user["email"], "id": user_id})
    
    safe_user = {k: v for k, v in new_user.items() if "password" not in k}
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": safe_user
    }


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest):
    user = get_user_by_email(payload.email)
    if not user:
        # Check if default demo student login
        if payload.email == "student@campusmind.ai" and payload.password == "Student@123":
            user = {
                "id": "std_001",
                "name": "Alex Johnson",
                "email": "student@campusmind.ai",
                "enrollmentNumber": "CS2022-8492",
                "department": "Computer Science & Engineering",
                "semester": "Semester 7",
                "section": "A",
                "cgpa": 8.74,
                "role": "student"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid university email or password."
            )
    else:
        # Check password
        is_valid = verify_password(payload.password, user.get("password_hash", ""))
        if not is_valid and user.get("plain_password_demo") != payload.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid university email or password."
            )

    token = create_access_token({"sub": user["email"], "id": user.get("id")})
    safe_user = {k: v for k, v in user.items() if "password" not in k}
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": safe_user
    }


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user.get("id", "std_001"),
        "name": current_user.get("name", "Alex Johnson"),
        "email": current_user.get("email", "student@campusmind.ai"),
        "enrollmentNumber": current_user.get("enrollmentNumber", "CS2022-8492"),
        "department": current_user.get("department", "Computer Science & Engineering"),
        "semester": current_user.get("semester", "Semester 7"),
        "section": current_user.get("section", "A"),
        "cgpa": current_user.get("cgpa", 8.74),
        "role": current_user.get("role", "student")
    }
