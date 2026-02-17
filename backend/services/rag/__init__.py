"""
RAG System Helper Functions

Factory functions for easy initialization of RAG components.
"""

from typing import Optional
from sqlalchemy.orm import Session

from .embeddings import EmbeddingService
from .retriever import DocumentRetriever
from .chain import RAGChain


# Singleton instances
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """
    Get singleton embedding service.
    
    Returns:
        EmbeddingService instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def get_document_retriever(db: Session, top_k: int = 5) -> DocumentRetriever:
    """
    Get document retriever with database session.
    
    Args:
        db: SQLAlchemy database session
        top_k: Number of results to return
        
    Returns:
        DocumentRetriever instance
    """
    return DocumentRetriever(db, top_k=top_k)


def create_rag_chain(
    db: Session,
    model: str = "gpt-4",
    system_prompt: Optional[str] = None
) -> RAGChain:
    """
    Create complete RAG chain with all components.
    
    Args:
        db: SQLAlchemy database session
        model: OpenAI model for generation
        system_prompt: Custom system prompt (optional)
        
    Returns:
        RAGChain instance ready to use
    """
    embedding_service = get_embedding_service()
    retriever = get_document_retriever(db)
    
    return RAGChain(
        embedding_service=embedding_service,
        retriever=retriever,
        model=model,
        system_prompt=system_prompt
    )


__all__ = [
    'get_embedding_service',
    'get_document_retriever',
    'create_rag_chain',
    'EmbeddingService',
    'DocumentRetriever',
    'RAGChain'
]
