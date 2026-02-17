"""
Simple Document Loader for Legal Documents

Loads text files into database with chunking for RAG system.
"""

import os
from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text


class SimpleDocumentLoader:
    """Simple loader for text documents without embeddings."""
    
    def __init__(self, db: Session, chunk_size: int = 1000):
        self.db = db
        self.chunk_size = chunk_size
    
    def load_document(
        self,
        file_path: str,
        practice_area: str,
        document_type: str = 'law',
        jurisdiction: str = 'SK'
    ) -> Tuple[int, int]:
        """
        Load a text document into the database.
        
        Returns: (document_id, chunks_count)
        """
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(file_path)
        
        # Insert document
        result = self.db.execute(text("""
            INSERT INTO documents (
                filename, file_path, practice_area, document_type, jurisdiction, 
                content, uploaded_at
            )
            VALUES (:filename, :file_path, :practice_area, :document_type, :jurisdiction,
                    :content, NOW())
            RETURNING id
        """), {
            'filename': filename,
            'file_path': file_path,
            'practice_area': practice_area,
            'document_type': document_type,
            'jurisdiction': jurisdiction,
            'content': content
        })
        
        doc_id = result.scalar()
        self.db.commit()
        
        # Create chunks
        chunks = self._chunk_text(content)
        chunks_count = 0
        
        for idx, chunk_text in enumerate(chunks):
            # Create zero vector for embedding (fallback)
            zero_vector = [0.0] * 1536
            
            # Convert metadata to JSON string
            import json
            metadata_json = json.dumps({'practice_area': practice_area})
            
            # Use raw connection to avoid SQLAlchemy escaping
            conn = self.db.connection().connection
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO document_chunks (
                    document_id, chunk_index, content, embedding, chunk_metadata
                )
                VALUES (%s, %s, %s, %s::vector, %s::jsonb)
            """, (doc_id, idx, chunk_text, str(zero_vector), metadata_json))
            chunks_count += 1
        
        self.db.commit()
        
        return doc_id, chunks_count
    
    def _chunk_text(self, text: str) -> list:
        """Split text into chunks."""
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1
            
            if current_length >= self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
