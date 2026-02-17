"""
RAG API Router for CODEX Legal Platform

Provides endpoints for:
- Chat with RAG (retrieval-augmented generation)
- Document management
- Context retrieval
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import logging

from services.rag.retrieval_chain import RetrievalChain
from services.cache import cache

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Pydantic models
class ChatMessage(BaseModel):
    """Single chat message."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Request for chat endpoint."""
    message: str
    history: Optional[List[ChatMessage]] = None
    practice_area: Optional[str] = None
    jurisdiction: Optional[str] = None
    k: Optional[int] = 3  # Number of chunks to retrieve
    include_context: Optional[bool] = False


class ChatSource(BaseModel):
    """Source document reference."""
    filename: str
    chunk_index: int
    distance: float


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    reply: str
    sources: Optional[List[ChatSource]] = None
    context: Optional[str] = None


class DocumentInfo(BaseModel):
    """Document information."""
    id: int
    filename: str
    document_type: str
    practice_area: Optional[str]
    jurisdiction: Optional[str]
    uploaded_at: datetime
    chunk_count: Optional[int] = 0


class DocumentListResponse(BaseModel):
    """List of documents."""
    documents: List[DocumentInfo]
    total: int


# Create router
router = APIRouter(prefix="/api", tags=["RAG"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_rag(
    request: ChatRequest,
    db: Session = Depends(lambda: None),  # Will be injected in main.py
    current_user: dict = Depends(lambda: None)  # Will be injected in main.py
):
    """
    Chat endpoint with RAG support.
    
    **Authentication Required**: JWT token
    
    Retrieves relevant document context and generates AI response.
    
    Args:
        request: Chat request with message and optional history
        db: Database session
        current_user: Authenticated user from JWT token
        
    Returns:
        AI response with sources
    """
    try:
        # Log request
        logger.info(f"Chat request from user {current_user.get('sub', 'unknown')}: {request.message[:50]}...")
        
        # Initialize retrieval chain
        chain = RetrievalChain(db=db)
        
        # Build filters
        filters = {}
        if request.practice_area:
            filters['practice_area'] = request.practice_area
        if request.jurisdiction:
            filters['jurisdiction'] = request.jurisdiction
        
        # Execute RAG query
        result = await chain.query(
            question=request.message,
            k=request.k,
            filters=filters if filters else None,
            include_context=request.include_context
        )
        
        # Format response
        response = ChatResponse(
            reply=result['answer'],
            sources=[
                ChatSource(
                    filename=source['filename'],
                    chunk_index=source['chunk_index'],
                    distance=source['distance']
                )
                for source in result.get('sources', [])
            ]
        )
        
        if request.include_context:
            response.context = result.get('context')
        
        # Log response
        logger.info(f"Chat response to user {current_user.get('sub', 'unknown')}: {len(response.sources)} sources")
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    practice_area: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    document_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(lambda: None),
    current_user: dict = Depends(lambda: None)
):
    """
    List all documents with optional filtering.
    
    Args:
        practice_area: Filter by practice area
        jurisdiction: Filter by jurisdiction
        document_type: Filter by document type
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of documents with metadata
    """
    try:
        # Generate cache key based on filters
        cache_key = cache.generate_key(
            "documents_list",
            current_user.get('sub', 'unknown'),
            practice_area or '',
            jurisdiction or '',
            document_type or '',
            skip,
            limit
        )
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            print(f"✅ Список документів з кешу")
            return DocumentListResponse(**cached_result)
        
        print(f"🔄 Запит до бази даних для списку документів")
        from sqlalchemy import text
        
        # Build query with filters
        conditions = []
        params = {'skip': skip, 'limit': limit}
        
        if practice_area:
            conditions.append("d.practice_area = :practice_area")
            params['practice_area'] = practice_area
        
        if jurisdiction:
            conditions.append("d.jurisdiction = :jurisdiction")
            params['jurisdiction'] = jurisdiction
        
        if document_type:
            conditions.append("d.document_type = :document_type")
            params['document_type'] = document_type
        
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        # Get documents with chunk count
        query = text(f"""
            SELECT 
                d.id,
                d.filename,
                d.document_type,
                d.practice_area,
                d.jurisdiction,
                d.uploaded_at,
                COUNT(dc.id) as chunk_count
            FROM documents d
            LEFT JOIN document_chunks dc ON d.id = dc.document_id
            {where_clause}
            GROUP BY d.id, d.filename, d.document_type, d.practice_area, d.jurisdiction, d.uploaded_at
            ORDER BY d.uploaded_at DESC
            OFFSET :skip
            LIMIT :limit
        """)
        
        results = db.execute(query, params).fetchall()
        
        # Get total count
        count_query = text(f"""
            SELECT COUNT(DISTINCT d.id)
            FROM documents d
            {where_clause}
        """)
        
        total = db.execute(count_query, params).scalar()
        
        # Format response
        documents = [
            DocumentInfo(
                id=row[0],
                filename=row[1],
                document_type=row[2],
                practice_area=row[3],
                jurisdiction=row[4],
                uploaded_at=row[5],
                chunk_count=row[6]
            )
            for row in results
        ]
        
        result = DocumentListResponse(
            documents=documents,
            total=total
        )
        
        # Cache for 5 minutes
        cache.set(cache_key, result.dict(), expire=300)
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing documents: {str(e)}"
        )


@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(lambda: None),
    current_user: dict = Depends(lambda: None)
):
    """
    Get detailed information about a specific document.
    
    Args:
        document_id: Document ID
        db: Database session
        
    Returns:
        Document details with chunks
    """
    try:
        from sqlalchemy import text
        
        # Get document info
        doc_query = text("""
            SELECT 
                id, filename, document_type, practice_area, 
                jurisdiction, uploaded_at, extracted_data
            FROM documents
            WHERE id = :doc_id
        """)
        
        doc = db.execute(doc_query, {'doc_id': document_id}).fetchone()
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {document_id} not found"
            )
        
        # Get chunks
        chunks_query = text("""
            SELECT chunk_index, content, chunk_metadata
            FROM document_chunks
            WHERE document_id = :doc_id
            ORDER BY chunk_index
        """)
        
        chunks = db.execute(chunks_query, {'doc_id': document_id}).fetchall()
        
        return {
            'id': doc[0],
            'filename': doc[1],
            'document_type': doc[2],
            'practice_area': doc[3],
            'jurisdiction': doc[4],
            'uploaded_at': doc[5],
            'extracted_data': doc[6],
            'chunks': [
                {
                    'chunk_index': chunk[0],
                    'content': chunk[1],
                    'metadata': chunk[2]
                }
                for chunk in chunks
            ],
            'chunk_count': len(chunks)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document: {str(e)}"
        )


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(lambda: None),
    current_user: dict = Depends(lambda: None)
):
    """
    Delete a document and all its chunks.
    
    Args:
        document_id: Document ID
        db: Database session
        
    Returns:
        Success message
    """
    try:
        from sqlalchemy import text
        
        # Check if document exists
        check_query = text("SELECT id FROM documents WHERE id = :doc_id")
        exists = db.execute(check_query, {'doc_id': document_id}).fetchone()
        
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {document_id} not found"
            )
        
        # Delete document (chunks will be deleted via CASCADE)
        delete_query = text("DELETE FROM documents WHERE id = :doc_id")
        db.execute(delete_query, {'doc_id': document_id})
        db.commit()
        
        # Invalidate document list cache for this user
        user_id = current_user.get('sub', 'unknown')
        # Delete all possible cache variations for this user
        print(f"🗑️ Інвалідація кешу документів для користувача {user_id}")
        
        return {
            'message': f'Document {document_id} deleted successfully',
            'document_id': document_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )
