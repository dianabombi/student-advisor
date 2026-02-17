"""
Student Advisor Platform - Vector Store Service

Handles document embeddings, chunking, and similarity search using pgvector.
Supports Retrieval-Augmented Generation (RAG) for legal document analysis.
"""

import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import openai
from sqlalchemy.orm import Session
from sqlalchemy import text, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base

# Text processing
try:
    import tiktoken
except ImportError:
    tiktoken = None

# Vector similarity
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Fallback if pgvector not installed
    Vector = None


class VectorStoreService:
    """
    Service for managing document embeddings and vector similarity search.
    
    Features:
    - Document chunking with configurable size and overlap
    - OpenAI embeddings generation
    - Semantic similarity search using pgvector
    - Metadata filtering for practice areas and jurisdictions
    """
    
    def __init__(
        self,
        db: Session,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize vector store service.
        
        Args:
            db: SQLAlchemy database session
            embedding_model: OpenAI embedding model to use
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Token overlap between chunks
        """
        self.db = db
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize tokenizer if available
        if tiktoken:
            try:
                self.tokenizer = tiktoken.encoding_for_model(embedding_model)
            except:
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
        else:
            self.tokenizer = None
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Rough estimation: ~4 chars per token
            return len(text) // 4
    
    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            para_tokens = self._count_tokens(paragraph)
            
            # If single paragraph exceeds chunk size, split by sentences
            if para_tokens > self.chunk_size:
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    sent_tokens = self._count_tokens(sentence)
                    
                    if current_tokens + sent_tokens > self.chunk_size and current_chunk:
                        chunks.append(current_chunk.strip())
                        # Keep overlap
                        overlap_text = current_chunk.split()[-self.chunk_overlap:]
                        current_chunk = ' '.join(overlap_text) + ' ' + sentence
                        current_tokens = self._count_tokens(current_chunk)
                    else:
                        current_chunk += ' ' + sentence
                        current_tokens += sent_tokens
            else:
                # Add paragraph to current chunk
                if current_tokens + para_tokens > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    # Keep overlap
                    overlap_text = current_chunk.split()[-self.chunk_overlap:]
                    current_chunk = ' '.join(overlap_text) + '\n\n' + paragraph
                    current_tokens = self._count_tokens(current_chunk)
                else:
                    current_chunk += '\n\n' + paragraph
                    current_tokens += para_tokens
        
        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI API.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.openai_api_key or self.openai_api_key == "your_key_here":
            # Return dummy embedding for testing without API key
            return [0.0] * 1536
        
        try:
            response = await openai.Embedding.acreate(
                model=self.embedding_model,
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536
    
    async def embed_document(
        self,
        document_id: int,
        text: str,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Create embeddings for a document and store in database.
        
        Args:
            document_id: ID of the document
            text: Full text content
            metadata: Additional metadata (practice_area, jurisdiction, etc.)
            
        Returns:
            Number of chunks created
        """
        # Chunk the text
        chunks = self._chunk_text(text)
        
        if not chunks:
            return 0
        
        metadata = metadata or {}
        chunks_created = 0
        
        # Process each chunk
        for idx, chunk_text in enumerate(chunks):
            # Generate embedding
            embedding = await self._generate_embedding(chunk_text)
            
            # Store in database
            # Note: This uses raw SQL because SQLAlchemy model is defined in main.py
            query = text("""
                INSERT INTO document_chunks 
                (document_id, chunk_index, content, embedding, metadata, created_at)
                VALUES (:doc_id, :idx, :content, :embedding, :metadata, :created_at)
            """)
            
            self.db.execute(query, {
                'doc_id': document_id,
                'idx': idx,
                'content': chunk_text,
                'embedding': embedding,
                'metadata': metadata,
                'created_at': datetime.utcnow()
            })
            chunks_created += 1
        
        self.db.commit()
        return chunks_created
    
    async def search_similar(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar document chunks using vector similarity.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional filters (practice_area, jurisdiction, document_id)
            
        Returns:
            List of similar chunks with metadata and similarity scores
        """
        # Generate query embedding
        query_embedding = await self._generate_embedding(query)
        
        # Build SQL query with optional filters
        filter_conditions = []
        params = {
            'query_embedding': query_embedding,
            'top_k': top_k
        }
        
        if filters:
            if 'practice_area' in filters:
                filter_conditions.append("metadata->>'practice_area' = :practice_area")
                params['practice_area'] = filters['practice_area']
            
            if 'jurisdiction' in filters:
                filter_conditions.append("metadata->>'jurisdiction' = :jurisdiction")
                params['jurisdiction'] = filters['jurisdiction']
            
            if 'document_id' in filters:
                filter_conditions.append("document_id = :document_id")
                params['document_id'] = filters['document_id']
        
        where_clause = ""
        if filter_conditions:
            where_clause = "WHERE " + " AND ".join(filter_conditions)
        
        # Cosine similarity search using pgvector
        query_sql = text(f"""
            SELECT 
                dc.id,
                dc.document_id,
                dc.chunk_index,
                dc.content,
                dc.metadata,
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
        similar_chunks = []
        for row in results:
            similar_chunks.append({
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
        
        return similar_chunks
    
    def delete_document_embeddings(self, document_id: int) -> int:
        """
        Delete all embeddings for a document.
        
        Args:
            document_id: ID of the document
            
        Returns:
            Number of chunks deleted
        """
        query = text("""
            DELETE FROM document_chunks
            WHERE document_id = :doc_id
        """)
        
        result = self.db.execute(query, {'doc_id': document_id})
        self.db.commit()
        
        return result.rowcount
    
    def get_document_chunks(self, document_id: int) -> List[Dict]:
        """
        Get all chunks for a document.
        
        Args:
            document_id: ID of the document
            
        Returns:
            List of chunks
        """
        query = text("""
            SELECT id, chunk_index, content, metadata, created_at
            FROM document_chunks
            WHERE document_id = :doc_id
            ORDER BY chunk_index
        """)
        
        results = self.db.execute(query, {'doc_id': document_id}).fetchall()
        
        chunks = []
        for row in results:
            chunks.append({
                'id': row[0],
                'chunk_index': row[1],
                'content': row[2],
                'metadata': row[3],
                'created_at': row[4]
            })
        
        return chunks
