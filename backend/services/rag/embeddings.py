"""
Document Retriever for Student Advisor RAG Module

Handles text embedding generation using OpenAI's embedding models.
Provides caching and batch processing capabilities.
"""

import os
from typing import List, Optional
import openai
from functools import lru_cache
from services.cache import cache


class EmbeddingService:
    """
    Service for generating text embeddings using OpenAI API.
    
    Features:
    - Automatic batching for efficiency
    - Caching for repeated queries
    - Fallback to zero vectors when API unavailable
    """
    
    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize embedding service.
        
        Args:
            model: OpenAI embedding model name
            api_key: OpenAI API key (defaults to env variable)
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.embedding_dimension = 1536  # OpenAI embedding dimension
        
        # Set OpenAI API key
        if self.api_key and self.api_key != "your_key_here":
            openai.api_key = self.api_key
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector (1536 dimensions)
        """
        if not self.api_key or self.api_key == "your_key_here":
            # Return zero vector as fallback
            return [0.0] * self.embedding_dimension
        
        # Try to get from Redis cache first
        cache_key = cache.generate_key("embedding", text)
        cached_embedding = cache.get(cache_key)
        
        if cached_embedding:
            print(f"✅ Embedding з кешу")
            return cached_embedding
        
        try:
            print(f"🔄 Генерую новий embedding")
            response = await openai.Embedding.acreate(
                model=self.model,
                input=text
            )
            embedding = response['data'][0]['embedding']
            
            # Store in Redis cache for 7 days
            cache.set(cache_key, embedding, expire=604800)
            
            return embedding
        except Exception as e:
            print(f"Embedding generation failed: {e}")
            return [0.0] * self.embedding_dimension
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not self.api_key or self.api_key == "your_key_here":
            return [[0.0] * self.embedding_dimension for _ in texts]
        
        try:
            response = await openai.Embedding.acreate(
                model=self.model,
                input=texts
            )
            return [item['embedding'] for item in response['data']]
        except Exception as e:
            print(f"Batch embedding generation failed: {e}")
            return [[0.0] * self.embedding_dimension for _ in texts]
    
    @lru_cache(maxsize=1000)
    def embed_text_cached(self, text: str) -> tuple:
        """
        Cached version of embed_text for frequently used queries.
        Returns tuple for hashability.
        """
        import asyncio
        embedding = asyncio.run(self.embed_text(text))
        return tuple(embedding)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this service."""
        return self.embedding_dimension
