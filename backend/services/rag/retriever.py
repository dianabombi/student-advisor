"""
Document Retriever for Student Advisor RAG Module

Handles vector similarity search and document chunk retrieval
from PostgreSQL with pgvector.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text


class DocumentRetriever:
    """
    Retrieves relevant document chunks using vector similarity search.
    
    Features:
    - Cosine similarity search with pgvector
    - Metadata filtering (practice area, jurisdiction, document type)
    - Configurable result count
    - Relevance scoring
    """
    
    def __init__(self, db: Session, top_k: int = 5):
        """
        Initialize document retriever.
        
        Args:
            db: SQLAlchemy database session
            top_k: Number of results to return
        """
        self.db = db
        self.top_k = top_k
    
    async def retrieve(
        self,
        query_embedding: List[float],
        filters: Optional[Dict] = None,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve relevant document chunks using vector similarity.
        
        Args:
            query_embedding: Query vector (1536 dimensions)
            filters: Optional filters (practice_area, jurisdiction, document_id)
            top_k: Override default number of results
            
        Returns:
            List of relevant chunks with metadata and similarity scores
        """
        k = top_k or self.top_k
        filters = filters or {}
        
        # Build filter conditions
        filter_conditions = []
        params = {
            'query_embedding': query_embedding,
            'top_k': k
        }
        
        if 'practice_area' in filters:
            filter_conditions.append("d.practice_area = :practice_area")
            params['practice_area'] = filters['practice_area']
        
        if 'jurisdiction' in filters:
            filter_conditions.append("d.jurisdiction = :jurisdiction")
            params['jurisdiction'] = filters['jurisdiction']
        
        if 'document_id' in filters:
            filter_conditions.append("dc.document_id = :document_id")
            params['document_id'] = filters['document_id']
        
        if 'document_type' in filters:
            filter_conditions.append("d.document_type = :document_type")
            params['document_type'] = filters['document_type']
        
        where_clause = ""
        if filter_conditions:
            where_clause = "WHERE " + " AND ".join(filter_conditions)
        
        # Execute similarity search
        query_sql = text(f"""
            SELECT 
                dc.id as chunk_id,
                dc.document_id,
                dc.chunk_index,
                dc.content,
                dc.chunk_metadata,
                d.filename,
                d.document_type,
                d.practice_area,
                d.jurisdiction,
                1 - (dc.embedding <=> :query_embedding) as similarity
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            {where_clause}
            ORDER BY dc.embedding <=> :query_embedding
            LIMIT :top_k
        """)
        
        results = self.db.execute(query_sql, params).fetchall()
        
        # Format results
        chunks = []
        for row in results:
            chunks.append({
                'chunk_id': row[0],
                'document_id': row[1],
                'chunk_index': row[2],
                'content': row[3],
                'metadata': row[4],
                'filename': row[5],
                'document_type': row[6],
                'practice_area': row[7],
                'jurisdiction': row[8],
                'similarity': float(row[9])
            })
        
        return chunks
    
    async def retrieve_by_document(
        self,
        document_id: int,
        query_embedding: List[float],
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve chunks from a specific document.
        
        Args:
            document_id: ID of the document
            query_embedding: Query vector
            top_k: Number of results
            
        Returns:
            List of relevant chunks from the document
        """
        return await self.retrieve(
            query_embedding=query_embedding,
            filters={'document_id': document_id},
            top_k=top_k
        )
    
    async def retrieve_by_practice_area(
        self,
        practice_area: str,
        query_embedding: List[float],
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve chunks from documents in a specific practice area.
        
        Args:
            practice_area: Practice area code (e.g., 'civil', 'criminal')
            query_embedding: Query vector
            top_k: Number of results
            
        Returns:
            List of relevant chunks from the practice area
        """
        return await self.retrieve(
            query_embedding=query_embedding,
            filters={'practice_area': practice_area},
            top_k=top_k
        )
    
    def get_chunk_context(self, chunk_id: int, context_size: int = 1) -> List[Dict]:
        """
        Get surrounding chunks for context.
        
        Args:
            chunk_id: ID of the central chunk
            context_size: Number of chunks before and after
            
        Returns:
            List of chunks including context
        """
        query_sql = text("""
            SELECT 
                dc.id,
                dc.content,
                dc.chunk_index
            FROM document_chunks dc
            WHERE dc.document_id = (
                SELECT document_id FROM document_chunks WHERE id = :chunk_id
            )
            AND dc.chunk_index BETWEEN 
                (SELECT chunk_index - :context_size FROM document_chunks WHERE id = :chunk_id)
                AND
                (SELECT chunk_index + :context_size FROM document_chunks WHERE id = :chunk_id)
            ORDER BY dc.chunk_index
        """)
        
        results = self.db.execute(
            query_sql,
            {'chunk_id': chunk_id, 'context_size': context_size}
        ).fetchall()
        
        return [
            {'id': row[0], 'content': row[1], 'chunk_index': row[2]}
            for row in results
        ]
