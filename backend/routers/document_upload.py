"""
Enhanced document upload endpoint with classification
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging
from pathlib import Path
import tempfile
import os

from services.document_classifier import DocumentClassifier

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/upload-with-classification")
async def upload_document_with_classification(
    file: UploadFile = File(...),
    db: Session = Depends(lambda: None),
    current_user: dict = Depends(lambda: None)
):
    """
    Upload document with automatic classification and key field extraction.
    
    **Authentication Required**: JWT token
    
    Process:
    1. Extract text from document (PDF, DOCX, TXT, or image via OCR)
    2. Classify document type
    3. Detect practice area
    4. Extract key fields (dates, amounts, parties)
    5. Store in database with metadata
    
    Args:
        file: Document file
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Document ID, classification results, and extracted fields
    """
    try:
        logger.info(f"Document upload by user {current_user.get('sub')}: {file.filename}")
        
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.txt', '.jpg', '.jpeg', '.png']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Extract text
            text_content = ""
            
            if file_ext == '.txt':
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            
            elif file_ext == '.pdf':
                import PyPDF2
                with open(tmp_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
            
            elif file_ext == '.docx':
                from docx import Document
                doc = Document(tmp_path)
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
            
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                # Use OCR (Mindee API)
                from services.ocr_service import extract_text_from_image
                text_content = await extract_text_from_image(tmp_path)
            
            if not text_content.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No text content could be extracted"
                )
            
            # Classify and extract fields
            classifier = DocumentClassifier()
            analysis = classifier.analyze_document(text_content, use_ai=True)
            
            # Store in database
            from sqlalchemy import text as sql_text
            from datetime import datetime
            
            insert_doc = sql_text("""
                INSERT INTO documents (
                    filename, file_path, document_type, practice_area,
                    jurisdiction, extracted_data, confidence, uploaded_at, user_id
                )
                VALUES (
                    :filename, :file_path, :doc_type, :practice_area,
                    :jurisdiction, :extracted_data, :confidence, :uploaded_at, :user_id
                )
                RETURNING id
            """)
            
            classification = analysis['classification']
            extracted_fields = analysis['extracted_fields']
            
            result = db.execute(insert_doc, {
                'filename': file.filename,
                'file_path': f"/uploads/{file.filename}",
                'doc_type': classification['document_type'],
                'practice_area': classification['practice_area'],
                'jurisdiction': 'SK',  # Default
                'extracted_data': {
                    'text': text_content[:1000],
                    'classification': classification,
                    'extracted_fields': extracted_fields,
                    'ai_extracted': analysis.get('ai_extracted', {})
                },
                'confidence': int(classification['type_confidence'] * 100),
                'uploaded_at': datetime.utcnow(),
                'user_id': current_user.get('id', 1)
            })
            
            document_id = result.fetchone()[0]
            db.commit()
            
            logger.info(f"Document {document_id} uploaded and classified: {classification['document_type']}")
            
            return {
                'document_id': document_id,
                'filename': file.filename,
                'classification': classification,
                'extracted_fields': {
                    'dates': extracted_fields['dates'][:5],  # Limit results
                    'amounts': extracted_fields['amounts'][:5],
                    'parties': extracted_fields['parties']
                },
                'ai_extracted': analysis.get('ai_extracted', {}),
                'message': 'Document uploaded and analyzed successfully'
            }
        
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )
