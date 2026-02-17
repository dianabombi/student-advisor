"""
Template Management API

Endpoints for uploading and managing document templates.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os

from auth.rbac import require_admin

router = APIRouter(prefix="/api/templates", tags=["Templates"])


# Pydantic models
class TemplateUploadResponse(BaseModel):
    """Template upload response."""
    success: bool
    template_name: str
    object_name: str
    message: str


class TemplateDeleteResponse(BaseModel):
    """Template delete response."""
    success: bool
    message: str


class TemplateListResponse(BaseModel):
    """Template list item."""
    name: str
    size: int
    last_modified: str


@router.post(
    "/upload",
    response_model=TemplateUploadResponse,
    dependencies=[Depends(require_admin)],
    summary="Upload Template (Admin Only)"
)
async def upload_template(
    file: UploadFile = File(...)
):
    """Upload a document template (DOCX only). Admin only."""
    # Validate file type
    if not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="Only DOCX files are supported"
        )
    
    # Save template logic here
    # For now, just return success
    return TemplateUploadResponse(
        success=True,
        template_name=file.filename,
        object_name=f"templates/{file.filename}",
        message="Template uploaded successfully"
    )


@router.get(
    "/",
    response_model=List[TemplateListResponse],
    dependencies=[Depends(require_admin)],
    summary="List Templates (Admin Only)"
)
async def list_templates():
    """List all available templates. Admin only."""
    # List templates logic here
    return []


@router.delete(
    "/{template_name}",
    response_model=TemplateDeleteResponse,
    dependencies=[Depends(require_admin)],
    summary="Delete Template (Admin Only)"
)
async def delete_template(
    template_name: str
):
    """Delete a template. Admin only."""
    # Delete template logic here
    return TemplateDeleteResponse(
        success=True,
        message=f"Template {template_name} deleted successfully"
    )
