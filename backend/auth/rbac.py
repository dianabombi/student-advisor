"""
Role-Based Access Control (RBAC) middleware for CODEX platform.

Provides decorators and dependencies for role verification.
"""

from enum import Enum
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class UserRole(str, Enum):
    """User roles enumeration."""
    USER = "user"
    ADMIN = "admin"
    PARTNER_LAWYER = "partner_lawyer"


# Database dependency (will be injected from main.py)
def get_db():
    """Database session dependency (placeholder)."""
    pass


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Get current user from JWT token.
    
    Extracts JWT from Authorization header, decodes it,
    and returns the user object.
    
    Raises:
        HTTPException 401: Invalid credentials
        HTTPException 403: Inactive user account
    """
    from main import User
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """
    Get current active user.
    
    Alias for get_current_user with explicit active check.
    """
    return current_user


def role_required(allowed_roles: List[UserRole]):
    """
    Dependency factory for role-based access control.
    
    Usage:
        @router.get("/admin/users")
        def get_users(current_user = Depends(role_required([UserRole.ADMIN]))):
            ...
    
    Args:
        allowed_roles: List of roles that can access this endpoint
        
    Returns:
        Dependency function that checks user role
        
    Raises:
        HTTPException 403: User doesn't have required role
    """
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


def require_admin(current_user = Depends(get_current_user)):
    """
    Dependency for admin-only endpoints.
    
    Usage:
        @router.get("/admin/dashboard")
        def admin_dashboard(current_user = Depends(require_admin)):
            ...
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_lawyer(current_user = Depends(get_current_user)):
    """
    Dependency for lawyer or admin endpoints.
    
    Allows both admin and partner_lawyer roles.
    
    Usage:
        @router.get("/lawyer/cases")
        def lawyer_cases(current_user = Depends(require_lawyer)):
            ...
    """
    if current_user.role not in [UserRole.ADMIN.value, UserRole.PARTNER_LAWYER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lawyer or admin access required"
        )
    return current_user


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Get current user if authenticated, otherwise None.
    
    Useful for endpoints that work with or without authentication.
    """
    if not token:
        return None
    
    try:
        return get_current_user(token, db)
    except HTTPException:
        return None


def verify_ownership(resource_user_id: int, current_user):
    """
    Verify that current user owns the resource or is admin.
    
    Args:
        resource_user_id: User ID of the resource owner
        current_user: Current authenticated user
        
    Raises:
        HTTPException 403: User doesn't own resource and is not admin
    """
    if current_user.role == UserRole.ADMIN.value:
        return True
    
    if current_user.id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
    
    return True


# Permission constants for different actions
class Permission(str, Enum):
    """Permission types for fine-grained access control."""
    # Document permissions
    VIEW_ANY_DOCUMENT = "view_any_document"
    EDIT_ANY_DOCUMENT = "edit_any_document"
    DELETE_ANY_DOCUMENT = "delete_any_document"
    
    # User management permissions
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    
    # Case permissions
    VIEW_ANY_CASE = "view_any_case"
    MANAGE_CASES = "manage_cases"
    
    # Template permissions
    MANAGE_TEMPLATES = "manage_templates"
    
    # System permissions
    VIEW_SYSTEM_LOGS = "view_system_logs"
    MANAGE_SETTINGS = "manage_settings"


# Role permissions mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.VIEW_ANY_DOCUMENT,
        Permission.EDIT_ANY_DOCUMENT,
        Permission.DELETE_ANY_DOCUMENT,
        Permission.MANAGE_USERS,
        Permission.MANAGE_ROLES,
        Permission.VIEW_ANY_CASE,
        Permission.MANAGE_CASES,
        Permission.MANAGE_TEMPLATES,
        Permission.VIEW_SYSTEM_LOGS,
        Permission.MANAGE_SETTINGS,
    ],
    UserRole.PARTNER_LAWYER: [
        Permission.VIEW_ANY_CASE,
        Permission.MANAGE_CASES,
        Permission.MANAGE_TEMPLATES,
    ],
    UserRole.USER: [
        # Users can only access their own resources
    ]
}


def has_permission(user, permission: Permission) -> bool:
    """
    Check if user has specific permission.
    
    Args:
        user: User object
        permission: Permission to check
        
    Returns:
        True if user has permission, False otherwise
    """
    user_role = UserRole(user.role)
    return permission in ROLE_PERMISSIONS.get(user_role, [])


def require_permission(permission: Permission):
    """
    Dependency factory for permission-based access control.
    
    Usage:
        @router.delete("/documents/{id}")
        def delete_document(
            id: int,
            current_user = Depends(require_permission(Permission.DELETE_ANY_DOCUMENT))
        ):
            ...
    """
    def permission_checker(current_user = Depends(get_current_user)):
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission.value}"
            )
        return current_user
    
    return permission_checker
