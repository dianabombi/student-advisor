# Document Processing API - Database Migration Guide

## Overview

This guide explains how to migrate from in-memory storage to database persistence for document processing jobs.

## Database Model

The `DocumentProcessingJob` model has been added to `main.py`:

```python
class DocumentProcessingJob(Base):
    __tablename__ = "document_processing_jobs"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True, nullable=False)  # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")
    progress = Column(Integer, default=0)
    
    # Processing results
    document_type = Column(String)
    confidence = Column(Float)
    extracted_fields = Column(JSON)
    summary = Column(Text)
    error_message = Column(Text)
    
    # MinIO paths
    raw_object_name = Column(String)
    processed_object_name = Column(String)
    filled_template_path = Column(String)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processing_started_at = Column(DateTime)
    processed_at = Column(DateTime)
    
    # Metadata
    metadata = Column(JSON)
    
    # Relationship
    user = relationship("User")
```

## Migration Steps

### 1. Update Imports in api/documents.py

Replace:
```python
from database.models import User
```

With:
```python
# Import User model from main.py where it's defined
import sys
sys.path.append('..')
from main import User, DocumentProcessingJob
```

### 2. Replace In-Memory Storage

**Before:**
```python
processing_status: Dict[str, Dict] = {}
```

**After:** Use database queries

### 3. Update upload_document Function

**Before:**
```python
processing_status[document_id] = {
    'document_id': document_id,
    'filename': file.filename,
    'status': 'pending',
    ...
}
```

**After:**
```python
job = DocumentProcessingJob(
    document_id=document_id,
    user_id=current_user.id,
    filename=file.filename,
    status='pending',
    raw_object_name=object_name,
    progress=0
)
db.add(job)
db.commit()
```

### 4. Update get_document_result Function

**Before:**
```python
if document_id not in processing_status:
    raise HTTPException(status_code=404, detail="Document not found")

status_data = processing_status[document_id]
```

**After:**
```python
job = db.query(DocumentProcessingJob).filter(
    DocumentProcessingJob.document_id == document_id
).first()

if not job:
    raise HTTPException(status_code=404, detail="Document not found")
```

### 5. Update list_documents Function

**Before:**
```python
for doc_id, doc_data in processing_status.items():
    if current_user.is_admin or doc_data.get('user_id') == current_user.id:
        ...
```

**After:**
```python
query = db.query(DocumentProcessingJob)

if not current_user.is_admin:
    query = query.filter(DocumentProcessingJob.user_id == current_user.id)

if status:
    query = query.filter(DocumentProcessingJob.status == status)

jobs = query.order_by(DocumentProcessingJob.uploaded_at.desc()).limit(limit).all()
```

### 6. Update process_document_pipeline Function

**Before:**
```python
processing_status[document_id]['status'] = 'processing'
processing_status[document_id]['progress'] = 10
```

**After:**
```python
# Get database session (need to pass it or create new one)
from database.database import SessionLocal
db = SessionLocal()

try:
    job = db.query(DocumentProcessingJob).filter(
        DocumentProcessingJob.document_id == document_id
    ).first()
    
    job.status = 'processing'
    job.progress = 10
    job.processing_started_at = datetime.utcnow()
    db.commit()
    
    # ... rest of processing ...
    
    job.status = 'completed'
    job.progress = 100
    job.processed_at = datetime.utcnow()
    db.commit()
    
finally:
    db.close()
```

## Complete Updated Functions

### upload_document with Database

```python
@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    auto_process: bool = True,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... validation ...
    
    document_id = str(uuid.uuid4())
    file_data = await file.read()
    
    object_name = storage.upload_raw_document(
        file_data=file_data,
        filename=file.filename,
        user_id=current_user.id,
        metadata={'document_id': document_id}
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
    
    if auto_process:
        background_tasks.add_task(
            process_document_pipeline,
            document_id,
            file_data,
            file.filename
        )
    
    return DocumentUploadResponse(
        success=True,
        document_id=document_id,
        message=f"Document '{file.filename}' uploaded successfully",
        status=job.status
    )
```

### get_document_result with Database

```python
@router.get("/{document_id}", response_model=DocumentResult)
async def get_document_result(
    document_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(DocumentProcessingJob).filter(
        DocumentProcessingJob.document_id == document_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if not current_user.is_admin and job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
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
    
    # Generate presigned URLs
    if job.status == 'completed':
        if job.raw_object_name:
            result.raw_document_url = storage.get_raw_document_url(job.raw_object_name)
        if job.processed_object_name:
            result.processed_document_url = storage.get_processed_document_url(job.processed_object_name)
    
    return result
```

### process_document_pipeline with Database

```python
async def process_document_pipeline(
    document_id: str,
    file_data: bytes,
    filename: str
):
    from database.database import SessionLocal
    db = SessionLocal()
    
    try:
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
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            text = perform_ocr(tmp_path)
            job.progress = 30
            db.commit()
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        # Step 2: Classification
        classification = classify_document(text)
        doc_type = classification['document_type']
        
        job.document_type = doc_type.value
        job.confidence = classification['confidence']
        job.progress = 50
        db.commit()
        
        # Step 3: Field Extraction
        fields = extract_document_fields(text, doc_type)
        
        job.extracted_fields = fields
        job.progress = 70
        db.commit()
        
        # Step 4: Save to MinIO
        processed_filename = f"{filename}_processed.txt"
        processed_object = storage.upload_processed_document(
            file_data=text.encode('utf-8'),
            filename=processed_filename,
            original_object_name=job.raw_object_name,
            processing_info={
                'document_type': doc_type.value,
                'confidence': job.confidence
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
```

## Benefits of Database Persistence

1. **Persistence** - Survives server restarts
2. **Scalability** - Can handle multiple workers
3. **Querying** - Advanced filtering and sorting
4. **Reliability** - ACID transactions
5. **History** - Complete audit trail

## Next Steps

1. Apply the migration changes to `api/documents.py`
2. Test the updated endpoints
3. Consider adding Celery for distributed task processing
4. Add database indexes for performance
5. Implement cleanup job for old records

---

**Note:** The current implementation uses in-memory storage. Apply these changes to enable database persistence.
