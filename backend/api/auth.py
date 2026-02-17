"""
Authentication API endpoints for CODEX platform.

Provides user registration, login, and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


# Pydantic models
class UserRegister(BaseModel):
    """User registration request."""
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str
    user: "UserProfile"


class UserProfile(BaseModel):
    """User profile response."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    phone: Optional[str] = None
    organization: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    """Registration success response."""
    success: bool
    message: str
    user: UserProfile


# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()  # Issued at
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Import dependencies
from main import get_db
from auth.rbac import get_current_user


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - **name**: User's full name
    - **email**: Unique email address
    - **password**: Password (will be hashed)
    
    Returns user profile and confirmation message.
    """
    from main import User
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user with default role 'user'
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user",  # Default role
        is_active=True,
        is_verified=False  # Require email verification
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create user profile response
    user_profile = UserProfile.from_orm(new_user)
    
    return RegisterResponse(
        success=True,
        message=f"User {new_user.email} registered successfully. Please verify your email.",
        user=user_profile
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get JWT token.
    
    - **username**: Email address
    - **password**: User password
    
    Returns JWT access token with user data.
    """
    from main import User
    
    # Find user by email (username field contains email)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact administrator."
        )
    
    # Create access token with user_id and role
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.id,  # Subject (user ID)
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified
        },
        expires_delta=access_token_expires
    )
    
    # Create user profile response with explicit fields
    user_profile = UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=False,  # Default value since User model doesn't have this field
        phone=getattr(user, 'phone', None),
        organization=getattr(user, 'organization', None),
        bio=getattr(user, 'bio', None),
        avatar_url=getattr(user, 'avatar_url', None),
        created_at=user.created_at
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_profile
    )


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user = Depends(get_current_user)
):
    """
    Get current user profile.
    
    Requires authentication token.
    Returns complete user profile data.
    """
    return UserProfile.from_orm(current_user)


@router.get("/me", response_model=UserProfile)
async def get_me(
    current_user = Depends(get_current_user)
):
    """
    Get current user data (alias for /profile).
    
    Requires authentication token.
    """
    return UserProfile.from_orm(current_user)


@router.post("/logout")
async def logout():
    """
    Logout user.
    
    Note: JWT tokens are stateless, so logout is handled on client side
    by removing the token. This endpoint is provided for API completeness.
    """
    return {
        "success": True,
        "message": "Logged out successfully. Please remove token from client."
    }


# Health check for auth service
@router.get("/health")
async def auth_health():
    """Check auth service health."""
    return {
        "status": "ok",
        "service": "authentication",
        "token_expiry_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    }
