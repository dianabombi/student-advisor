"""
Authentication dependencies for easy import.

Provides centralized access to all auth-related dependencies.
"""

from .rbac import (
    # Dependencies
    get_current_user,
    get_current_active_user,
    get_optional_user,
    
    # Role checks
    role_required,
    require_admin,
    require_lawyer,
    
    # Permission checks
    require_permission,
    has_permission,
    verify_ownership,
    
    # Enums
    UserRole,
    Permission,
)

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_optional_user",
    "role_required",
    "require_admin",
    "require_lawyer",
    "require_permission",
    "has_permission",
    "verify_ownership",
    "UserRole",
    "Permission",
]
