"""
Cases API Endpoints

Provides CRUD operations for legal cases with filtering, pagination, and detailed views.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Text, Integer, DECIMAL, TIMESTAMP
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import enum

from auth.rbac import get_current_user
from main import get_db, Base, User

router = APIRouter(prefix="/api/cases", tags=["Cases"])


# Enums
class CaseStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    under_review = "under_review"
    hearing_scheduled = "hearing_scheduled"
    resolved = "resolved"
    cancelled = "cancelled"


# Status transition rules
ALLOWED_TRANSITIONS = {
    'draft': ['submitted', 'cancelled'],
    'submitted': ['under_review', 'cancelled'],
    'under_review': ['hearing_scheduled', 'resolved', 'cancelled'],
    'hearing_scheduled': ['resolved', 'cancelled'],
    'resolved': [],
    'cancelled': []
}


# SQLAlchemy Models
class Case(Base):
    __tablename__ = "cases"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String, default="draft", nullable=False)
    assigned_to = Column(Integer)
    deadline = Column(TIMESTAMP)
    claim_amount = Column(DECIMAL(15, 2))
    priority = Column(String(20), default="medium")
    client_name = Column(String(255))
    client_email = Column(String(255))
    client_phone = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class CaseLog(Base):
    __tablename__ = "case_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    case_id = Column(String, nullable=False)
    event_time = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    event_type = Column(String(50), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    created_by = Column(Integer, nullable=False)
    comment = Column(Text)


class CaseDocument(Base):
    __tablename__ = "case_documents"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    case_id = Column(String, nullable=False)
    file_name = Column(String(500), nullable=False)
    file_key = Column(String(1000), nullable=False)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    uploaded_by = Column(Integer)


# Pydantic Models
class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    claim_amount: Optional[float] = None
    priority: Optional[str] = "medium"
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    claim_amount: Optional[float] = None
    priority: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None


class StatusChange(BaseModel):
    new_status: str


class AssignLawyer(BaseModel):
    lawyer_id: int


class AddNote(BaseModel):
    comment: str


class CaseResponse(BaseModel):
    id: str
    user_id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: Optional[int]
    deadline: Optional[datetime]
    claim_amount: Optional[float]
    priority: str
    client_name: Optional[str]
    client_email: Optional[str]
    client_phone: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CaseLogResponse(BaseModel):
    id: str
    case_id: str
    event_time: datetime
    event_type: str
    old_value: Optional[str]
    new_value: Optional[str]
    created_by: int
    comment: Optional[str]
    
    class Config:
        from_attributes = True


class CaseDocumentResponse(BaseModel):
    id: str
    case_id: str
    file_name: str
    file_key: str
    uploaded_at: datetime
    uploaded_by: Optional[int]
    
    class Config:
        from_attributes = True


class CaseDetailResponse(CaseResponse):
    logs: List[CaseLogResponse] = []
    documents: List[CaseDocumentResponse] = []


# API Endpoints

@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new legal case with status 'draft'."""
    new_case = Case(
        user_id=current_user.id,
        title=case_data.title,
        description=case_data.description,
        status="draft",
        deadline=case_data.deadline,
        claim_amount=case_data.claim_amount,
        priority=case_data.priority or "medium",
        client_name=case_data.client_name,
        client_email=case_data.client_email,
        client_phone=case_data.client_phone
    )
    
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    
    log_entry = CaseLog(
        case_id=str(new_case.id),
        event_type="created",
        new_value="draft",
        created_by=current_user.id,
        comment="Case created"
    )
    db.add(log_entry)
    db.commit()
    
    return new_case


@router.get("", response_model=List[CaseResponse])
async def list_cases(
    status: Optional[str] = Query(None),
    assigned: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of cases with filters and pagination."""
    query = db.query(Case)
    
    if current_user.role in ['admin', 'partner_lawyer', 'lawyer']:
        if assigned:
            query = query.filter(Case.assigned_to == current_user.id)
        elif current_user.role != 'admin':
            query = query.filter(Case.assigned_to == current_user.id)
    else:
        query = query.filter(Case.user_id == current_user.id)
    
    if status:
        query = query.filter(Case.status == status)
    
    offset = (page - 1) * page_size
    cases = query.order_by(Case.created_at.desc()).offset(offset).limit(page_size).all()
    
    return cases


@router.get("/{case_id}", response_model=CaseDetailResponse)
async def get_case(
    case_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get case details with logs and documents."""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if current_user.role not in ['admin', 'partner_lawyer']:
        if case.user_id != current_user.id and case.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    logs = db.query(CaseLog).filter(CaseLog.case_id == case_id).order_by(CaseLog.event_time.desc()).all()
    documents = db.query(CaseDocument).filter(CaseDocument.case_id == case_id).order_by(CaseDocument.uploaded_at.desc()).all()
    
    case_dict = {
        "id": case.id,
        "user_id": case.user_id,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "assigned_to": case.assigned_to,
        "deadline": case.deadline,
        "claim_amount": float(case.claim_amount) if case.claim_amount else None,
        "priority": case.priority,
        "client_name": case.client_name,
        "client_email": case.client_email,
        "client_phone": case.client_phone,
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        "logs": logs,
        "documents": documents
    }
    
    return case_dict


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: str,
    case_data: CaseUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update case fields. Users can edit own drafts, admins/lawyers can edit any field."""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    is_admin_or_lawyer = current_user.role in ['admin', 'partner_lawyer', 'lawyer']
    is_owner = case.user_id == current_user.id
    is_draft = case.status == 'draft'
    
    if not is_admin_or_lawyer:
        if not is_owner:
            raise HTTPException(status_code=403, detail="Not authorized")
        if not is_draft:
            raise HTTPException(status_code=403, detail="Can only edit draft cases")
    
    update_data = case_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(case, field, value)
    
    case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(case)
    
    updated_fields = ", ".join(update_data.keys())
    log_entry = CaseLog(
        case_id=case_id,
        event_type='updated',
        created_by=current_user.id,
        comment=f"Case updated: {updated_fields}"
    )
    db.add(log_entry)
    db.commit()
    
    return case


@router.post("/{case_id}/status", response_model=CaseResponse)
async def change_status(
    case_id: str,
    status_data: StatusChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change case status with validation of allowed transitions."""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    current_status = case.status
    new_status = status_data.new_status
    
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )
    
    old_status = case.status
    case.status = new_status
    case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(case)
    
    log_entry = CaseLog(
        case_id=case_id,
        event_type='status_change',
        old_value=old_status,
        new_value=new_status,
        created_by=current_user.id,
        comment=f"Status changed from {old_status} to {new_status}"
    )
    db.add(log_entry)
    db.commit()
    
    return case


@router.post("/{case_id}/assign", response_model=CaseResponse)
async def assign_lawyer(
    case_id: str,
    assign_data: AssignLawyer,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign a lawyer to a case. Only admins can assign lawyers."""
    if current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Only admins can assign lawyers")
    
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    lawyer = db.query(User).filter(User.id == assign_data.lawyer_id).first()
    
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    
    if lawyer.role not in ['lawyer', 'partner_lawyer']:
        raise HTTPException(status_code=400, detail="User is not a lawyer")
    
    old_lawyer = case.assigned_to
    case.assigned_to = assign_data.lawyer_id
    case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(case)
    
    log_entry = CaseLog(
        case_id=case_id,
        event_type='assignment',
        old_value=str(old_lawyer) if old_lawyer else None,
        new_value=str(assign_data.lawyer_id),
        created_by=current_user.id,
        comment=f"Lawyer {lawyer.name} assigned to case"
    )
    db.add(log_entry)
    db.commit()
    
    return case


@router.post("/{case_id}/notes", status_code=status.HTTP_201_CREATED)
async def add_note(
    case_id: str,
    note_data: AddNote,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a note/comment to the case log."""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    log_entry = CaseLog(
        case_id=case_id,
        event_type='note',
        created_by=current_user.id,
        comment=note_data.comment
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    return {
        'success': True,
        'message': 'Note added successfully',
        'log_id': log_entry.id
    }


# Document Management Endpoints (Task 4.3.c)

from fastapi import UploadFile, File
import uuid
import os


@router.post('/{case_id}/documents', status_code=status.HTTP_201_CREATED)
async def upload_document(
    case_id: str,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    '''
    Upload a document/file for a case.
    
    File is stored in MinIO and metadata in case_documents table.
    '''
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    
    # Check permissions
    if current_user.role not in ['admin', 'partner_lawyer', 'lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='Not authorized')
    
    # Generate unique file key for MinIO
    file_extension = os.path.splitext(file.filename)[1]
    file_key = f'cases/{case_id}/{uuid.uuid4()}{file_extension}'
    
    # Read file content
    file_content = await file.read()
    
    # Store in MinIO (using existing MinIO service)
    try:
        from services.doc_processor.storage import MinIOStorage
        storage = MinIOStorage()
        storage.upload_file(file_key, file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to upload file: {str(e)}')
    
    # Save metadata to database
    doc_entry = CaseDocument(
        case_id=case_id,
        file_name=file.filename,
        file_key=file_key,
        uploaded_by=current_user.id
    )
    db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)
    
    # Log upload
    log_entry = CaseLog(
        case_id=case_id,
        event_type='document_uploaded',
        new_value=file.filename,
        created_by=current_user.id,
        comment=f'Document uploaded: {file.filename}'
    )
    db.add(log_entry)
    db.commit()
    
    return {
        'success': True,
        'message': 'Document uploaded successfully',
        'document': {
            'id': doc_entry.id,
            'file_name': doc_entry.file_name,
            'file_key': doc_entry.file_key,
            'uploaded_at': doc_entry.uploaded_at,
            'uploaded_by': doc_entry.uploaded_by
        }
    }


@router.get('/{case_id}/documents', response_model=List[CaseDocumentResponse])
async def list_documents(
    case_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    '''
    Get list of documents attached to a case.
    '''
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    
    # Check permissions
    if current_user.role not in ['admin', 'partner_lawyer']:
        if case.user_id != current_user.id and case.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail='Not authorized')
    
    # Get documents
    documents = db.query(CaseDocument).filter(
        CaseDocument.case_id == case_id
    ).order_by(CaseDocument.uploaded_at.desc()).all()
    
    return documents


@router.delete('/{case_id}/documents/{doc_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    case_id: str,
    doc_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    '''
    Delete a document from a case.
    
    Removes file from MinIO and database record.
    '''
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    
    # Check permissions (only admins or case owner)
    if current_user.role not in ['admin', 'partner_lawyer']:
        if case.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='Not authorized')
    
    # Get document
    document = db.query(CaseDocument).filter(
        CaseDocument.id == doc_id,
        CaseDocument.case_id == case_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    
    # Delete from MinIO
    try:
        from services.doc_processor.storage import MinIOStorage
        storage = MinIOStorage()
        storage.delete_file(document.file_key)
    except Exception as e:
        # Log error but continue with database deletion
        print(f'Warning: Failed to delete file from MinIO: {e}')
    
    # Delete from database
    file_name = document.file_name
    db.delete(document)
    db.commit()
    
    # Log deletion
    log_entry = CaseLog(
        case_id=case_id,
        event_type='document_deleted',
        old_value=file_name,
        created_by=current_user.id,
        comment=f'Document deleted: {file_name}'
    )
    db.add(log_entry)
    db.commit()
    
    return None


# Timeline Endpoint (Task 4.3.d)

@router.get('/{case_id}/timeline', response_model=List[CaseLogResponse])
async def get_timeline(
    case_id: str,
    event_type: Optional[str] = Query(None, description='Filter by event type'),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    '''
    Get chronological timeline of case events.
    
    - **event_type**: Optional filter (status_change, note, assignment, etc.)
    
    Returns events in chronological order (newest first).
    '''
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail='Case not found')
    
    # Check permissions
    if current_user.role not in ['admin', 'partner_lawyer']:
        if case.user_id != current_user.id and case.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail='Not authorized')
    
    # Build query
    query = db.query(CaseLog).filter(CaseLog.case_id == case_id)
    
    # Filter by event type if specified
    if event_type:
        query = query.filter(CaseLog.event_type == event_type)
    
    # Get logs in chronological order (newest first)
    logs = query.order_by(CaseLog.event_time.desc()).all()
    
    return logs
