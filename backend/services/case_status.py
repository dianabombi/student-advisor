"""
Case Status Management and Validation

Defines allowed status transitions and validation logic.
"""

from typing import Dict, List, Optional
from datetime import datetime


# Status transition rules (Task 4.4.a)
ALLOWED_TRANSITIONS: Dict[str, List[str]] = {
    'draft': ['submitted', 'cancelled'],
    'submitted': ['under_review', 'cancelled'],
    'under_review': ['hearing_scheduled', 'resolved', 'cancelled'],
    'hearing_scheduled': ['resolved', 'cancelled'],
    'resolved': [],  # Terminal state
    'cancelled': []  # Terminal state
}


def validate_status_transition(current_status: str, new_status: str) -> tuple[bool, Optional[str]]:
    """
    Validate if status transition is allowed.
    
    Args:
        current_status: Current case status
        new_status: Desired new status
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if current status exists
    if current_status not in ALLOWED_TRANSITIONS:
        return False, f"Invalid current status: {current_status}"
    
    # Check if transition is allowed
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    
    if new_status not in allowed:
        if not allowed:
            return False, f"Status '{current_status}' is terminal and cannot be changed"
        return False, f"Cannot transition from '{current_status}' to '{new_status}'. Allowed: {', '.join(allowed)}"
    
    return True, None


def get_allowed_transitions(current_status: str) -> List[str]:
    """
    Get list of allowed status transitions from current status.
    
    Args:
        current_status: Current case status
        
    Returns:
        List of allowed next statuses
    """
    return ALLOWED_TRANSITIONS.get(current_status, [])


def is_terminal_status(status: str) -> bool:
    """
    Check if status is terminal (no further transitions allowed).
    
    Args:
        status: Status to check
        
    Returns:
        True if terminal status
    """
    return len(ALLOWED_TRANSITIONS.get(status, [])) == 0


# Status descriptions for documentation
STATUS_DESCRIPTIONS = {
    'draft': 'Case is being prepared by the client',
    'submitted': 'Case has been submitted and awaiting review',
    'under_review': 'Case is being reviewed by a lawyer',
    'hearing_scheduled': 'Court hearing has been scheduled',
    'resolved': 'Case has been resolved (terminal)',
    'cancelled': 'Case has been cancelled (terminal)'
}


def get_status_description(status: str) -> str:
    """Get human-readable description of a status."""
    return STATUS_DESCRIPTIONS.get(status, 'Unknown status')
