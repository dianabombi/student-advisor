"""
Document Processing API

Endpoints for document upload and processing with database persistence.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from typing import Optional, Dict, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import uuid
from datetime import datetime
import tempfile
import os

from services.doc_processor import (
    perform_ocr,
    classify_document,
    extract_document_fields,
    DocumentType,
    MinIOStorage
)
from auth.rbac import get_current_user, require_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


# Import models from main.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import User, DocumentProcessingJob


# Pydantic models
class DocumentUploadResponse(BaseModel):
    """Document upload response."""
    success: bool
    document_id: str
    message: str
    status: str


class DocumentProcessingStatus(BaseModel):
    """Document processing status."""
    document_id: str
    status: str  # pending, processing, completed, failed
    filename: str
    uploaded_at: str
    processed_at: Optional[str] = None
    progress: int  # 0-100


class DocumentResult(BaseModel):
    """Document processing result."""
    document_id: str
    filename: str
    status: str
    document_type: Optional[str] = None
    confidence: Optional[float] = None
    extracted_fields: Optional[Dict] = None
    raw_document_url: Optional[str] = None
    processed_document_url: Optional[str] = None
    filled_template_url: Optional[str] = None
    summary: Optional[str] = None
    error: Optional[str] = None


# Initialize services
storage = MinIOStorage()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    auto_process: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload document for processing.
    
    Args:
        file: Document file (PDF, JPG, PNG, TIFF)
        auto_process: Automatically start processing pipeline
        
    Returns:
        Upload response with document ID
    """
    try:
        logger.info(f"Document upload by user {current_user.email}: {file.filename}")
        
        # Validate file type
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif']
        file_ext = '.' + file.filename.split('.')[-1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Generate document ID
        document_id = str(uuid.uuid4())
        
        # Read file data
        file_data = await file.read()
        
        # Upload to MinIO raw-docs bucket
        object_name = storage.upload_raw_document(
            file_data=file_data,
            filename=file.filename,
            user_id=current_user.id,
            metadata={
                'document_id': document_id,
                'uploaded_by': current_user.email,
                'uploaded_at': datetime.utcnow().isoformat()
            }
        )
        
        # Create database record
        job = DocumentProcessingJob(
            document_id=document_id,
            user_id=current_user.id,
            filename=file.filename,
            status='pending' if not auto_process else 'processing',
            raw_object_name=object_name,
            progress=0
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Start processing in background if requested
        if auto_process:
            background_tasks.add_task(
                process_document_pipeline,
                document_id,
                file_data,
                file.filename
            )
        
        logger.info(f"Document uploaded: {document_id}")
        
        return DocumentUploadResponse(
            success=True,
            document_id=document_id,
            message=f"Document '{file.filename}' uploaded successfully",
            status=job.status
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentResult)
async def get_document_result(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document processing result.
    
    Args:
        document_id: Document ID
        
    Returns:
        Processing result with extracted data
    """
    try:
        logger.info(f"Getting document result: {document_id}")
        
        # Get job from database
        job = db.query(DocumentProcessingJob).filter(
            DocumentProcessingJob.document_id == document_id
        ).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Check user access (admin can see all, users only their own)
        if not current_user.is_admin and job.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Build result
        result = DocumentResult(
            document_id=job.document_id,
            filename=job.filename,
            status=job.status,
            document_type=job.document_type,
            confidence=job.confidence,
            extracted_fields=job.extracted_fields,
            summary=job.summary,
            error=job.error_message
        )
        
        # Add processing results if completed
        if job.status == 'completed':
            result.processed_at = job.processed_at.isoformat() if job.processed_at else None
            
            # Generate presigned URLs
            if job.raw_object_name:
                result.raw_document_url = storage.get_presigned_url(
                    storage.BUCKET_RAW,
                    job.raw_object_name
                )
            
            if job.processed_object_name:
                result.processed_document_url = storage.get_presigned_url(
                    storage.BUCKET_PROCESSED,
                    job.processed_object_name
                )
            
            if job.filled_template_path:
                result.filled_template_url = job.filled_template_path
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}/status", response_model=DocumentProcessingStatus)
async def get_document_status(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document processing status.
    
    Args:
        document_id: Document ID
        
    Returns:
        Processing status
    """
    try:
        # Get job from database
        job = db.query(DocumentProcessingJob).filter(
            DocumentProcessingJob.document_id == document_id
        ).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Check user access
        if not current_user.is_admin and job.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return DocumentProcessingStatus(
            document_id=job.document_id,
            status=job.status,
            filename=job.filename,
            uploaded_at=job.uploaded_at.isoformat(),
            processed_at=job.processed_at.isoformat() if job.processed_at else None,
            progress=job.progress
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DocumentProcessingStatus])
async def list_documents(
    status: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's documents.
    
    Args:
        status: Filter by status (pending, processing, completed, failed)
        limit: Maximum number of documents to return
        
    Returns:
        List of documents
    """
    try:
        # Build query
        query = db.query(DocumentProcessingJob)
        
        # Admin sees all, users see only their own
        if not current_user.is_admin:
            query = query.filter(DocumentProcessingJob.user_id == current_user.id)
        
        # Apply status filter if provided
        if status:
            query = query.filter(DocumentProcessingJob.status == status)
        
        # Order by upload time (newest first) and limit
        jobs = query.order_by(
            DocumentProcessingJob.uploaded_at.desc()
        ).limit(limit).all()
        
        # Convert to response model
        return [
            DocumentProcessingStatus(
                document_id=job.document_id,
                status=job.status,
                filename=job.filename,
                uploaded_at=job.uploaded_at.isoformat(),
                processed_at=job.processed_at.isoformat() if job.processed_at else None,
                progress=job.progress
            )
            for job in jobs
        ]
    
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete document and its processing results.
    
    Args:
        document_id: Document ID
        
    Returns:
        Success message
    """
    try:
        # Get job from database
        job = db.query(DocumentProcessingJob).filter(
            DocumentProcessingJob.document_id == document_id
        ).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Check user access
        if not current_user.is_admin and job.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Delete from MinIO
        if job.raw_object_name:
            try:
                storage.delete_file(storage.BUCKET_RAW, job.raw_object_name)
            except Exception as e:
                logger.warning(f"Failed to delete raw file: {e}")
        
        if job.processed_object_name:
            try:
                storage.delete_file(storage.BUCKET_PROCESSED, job.processed_object_name)
            except Exception as e:
                logger.warning(f"Failed to delete processed file: {e}")
        
        # Delete from database
        db.delete(job)
        db.commit()
        
        logger.info(f"Document deleted: {document_id}")
        
        return {"success": True, "message": "Document deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Background processing function
async def process_document_pipeline(
    document_id: str,
    file_data: bytes,
    filename: str
):
    """
    Process document through complete pipeline.
    
    Pipeline:
    1. OCR - Extract text
    2. Classification - Determine document type
    3. Field Extraction - Extract key fields
    4. Storage - Save to MinIO
    5. Summary - Generate summary
    """
    # Create new database session for background task
    db = SessionLocal()
    
    try:
        logger.info(f"Starting pipeline for document: {document_id}")
        
        # Get job from database
        job = db.query(DocumentProcessingJob).filter(
            DocumentProcessingJob.document_id == document_id
        ).first()
        
        if not job:
            logger.error(f"Job not found: {document_id}")
            return
        
        # Update status
        job.status = 'processing'
        job.progress = 10
        job.processing_started_at = datetime.utcnow()
        db.commit()
        
        # Step 1: OCR
        logger.info(f"Step 1: OCR for {document_id}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            text = perform_ocr(tmp_path)
            job.progress = 30
            db.commit()
            logger.info(f"OCR completed: {len(text)} characters")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        # Step 2: Classification
        logger.info(f"Step 2: Classification for {document_id}")
        classification = classify_document(text)
        doc_type = classification['document_type']
        confidence = classification['confidence']
        
        job.document_type = doc_type.value
        job.confidence = confidence
        job.progress = 50
        db.commit()
        
        logger.info(f"Classification: {doc_type.value} (confidence: {confidence:.2%})")
        
        # Step 3: Field Extraction
        logger.info(f"Step 3: Field extraction for {document_id}")
        fields = extract_document_fields(text, doc_type)
        
        job.extracted_fields = fields
        job.progress = 70
        db.commit()
        
        logger.info(f"Extracted {fields.get('_metadata', {}).get('field_count', 0)} fields")
        
        # Step 4: Save processed text to MinIO
        processed_filename = f"{filename}_processed.txt"
        processed_object = storage.upload_processed_document(
            file_data=text.encode('utf-8'),
            filename=processed_filename,
            original_object_name=job.raw_object_name,
            processing_info={
                'document_type': doc_type.value,
                'confidence': confidence,
                'field_count': fields.get('_metadata', {}).get('field_count', 0)
            }
        )
        
        job.processed_object_name = processed_object
        job.progress = 90
        db.commit()
        
        # Step 5: Generate summary
        from services.doc_processor import TemplateFiller
        filler = TemplateFiller()
        summary = filler.generate_summary({
            'classification': {'document_type': doc_type.value},
            'parties': fields.get('parties', []),
            'dates': fields.get('dates', []),
            'amounts': fields.get('amounts', []),
            'identifiers': fields.get('identifiers', {})
        })
        
        job.summary = summary
        job.status = 'completed'
        job.progress = 100
        job.processed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Pipeline completed for document: {document_id}")
    
    except Exception as e:
        logger.error(f"Pipeline failed for {document_id}: {e}")
        if job:
            job.status = 'failed'
            job.error_message = str(e)
            job.progress = 0
            db.commit()
    
    finally:
        db.close()
