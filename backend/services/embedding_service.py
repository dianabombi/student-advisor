#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Embedding Service
Generates vector embeddings using OpenAI for RAG
"""

import os
import json
from typing import List, Dict
from openai import AsyncOpenAI
from sqlalchemy.orm import Session


class EmbeddingService:
    """Service for generating and storing vector embeddings"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-ada-002"
        self.dimension = 1536
        
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Truncate text if too long (max 8191 tokens for ada-002)
            if len(text) > 30000:  # Rough estimate
                text = text[:30000]
            
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def store_embedding(
        self, 
        db: Session, 
        content_id: int, 
        embedding: List[float]
    ) -> bool:
        """
        Store embedding in database
        
        Args:
            db: Database session
            content_id: Content ID
            embedding: Embedding vector
            
        Returns:
            True if successful
        """
        from main import UniversityEmbedding
        
        try:
            # Convert embedding to JSON string for storage
            embedding_json = json.dumps(embedding)
            
            # Check if embedding already exists
            existing = db.query(UniversityEmbedding).filter_by(
                content_id=content_id
            ).first()
            
            if existing:
                existing.embedding = embedding_json
            else:
                new_embedding = UniversityEmbedding(
                    content_id=content_id,
                    embedding=embedding_json
                )
                db.add(new_embedding)
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error storing embedding: {e}")
            db.rollback()
            return False
    
    async def batch_generate_embeddings(
        self, 
        db: Session, 
        content_ids: List[int]
    ) -> Dict:
        """
        Generate embeddings for multiple content items
        
        Args:
            db: Database session
            content_ids: List of content IDs
            
        Returns:
            Dict with results
        """
        from main import UniversityContent
        
        success_count = 0
        error_count = 0
        
        for content_id in content_ids:
            try:
                # Get content
                content = db.query(UniversityContent).filter_by(id=content_id).first()
                if not content:
                    continue
                
                # Generate embedding
                embedding = await self.generate_embedding(content.content)
                
                if embedding:
                    # Store embedding
                    await self.store_embedding(db, content_id, embedding)
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                print(f"Error processing content {content_id}: {e}")
                error_count += 1
        
        return {
            'success_count': success_count,
            'error_count': error_count,
            'total': len(content_ids)
        }
