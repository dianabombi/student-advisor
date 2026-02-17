"""
CODEX Legal Platform - Configuration Package
"""

from .practice_areas import (
    PRACTICE_AREAS,
    LEGAL_DOCUMENT_TYPES,
    JURISDICTIONS,
    get_practice_area_name,
    get_document_type_name,
    get_enabled_jurisdictions
)

__all__ = [
    "PRACTICE_AREAS",
    "LEGAL_DOCUMENT_TYPES",
    "JURISDICTIONS",
    "get_practice_area_name",
    "get_document_type_name",
    "get_enabled_jurisdictions"
]
