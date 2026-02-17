#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Service - Updated
Retrieval Augmented Generation for university chat
Searches in ANY language (website language), AI translates to user language
"""

import json
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from services.embedding_service import EmbeddingService


class RAGService:
    """Service for retrieving relevant content using RAG"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    async def search_any_language_content(
        self,
        db: Session,
        university_id: int,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for relevant content in ANY language (website's language)
        AI will translate the content to user's language
        
        Args:
            db: Database session
            university_id: University ID
            query: User's question
            top_k: Number of results to return
            
        Returns:
            List of relevant content items
        """
        try:
            print(f"RAG: Searching ANY language for university_id={university_id}")
            
            # Simple query - get any content for this university
            sql = text("""
                SELECT 
                    uc.id,
                    uc.title,
                    uc.content,
                    uc.url,
                    uc.content_type,
                    uc.language
                FROM university_content uc
                WHERE uc.university_id = :university_id
                  AND uc.is_active = TRUE
                ORDER BY uc.id
                LIMIT :top_k
            """)
            
            result = db.execute(sql, {
                'university_id': university_id,
                'top_k': top_k
            })
            
            results = []
            for row in result:
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'url': row[3],
                    'content_type': row[4],
                    'language': row[5],
                    'similarity': 1.0
                })
            
            print(f"RAG: Found {len(results)} results in ANY language")
            return results
            
        except Exception as e:
            print(f"Error searching content: {e}")
            return []
    
    def format_context_for_prompt(self, results: List[Dict]) -> str:
        """
        Format search results into context for AI prompt
        
        Args:
            results: Search results
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found in the university database."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            # Include language info so AI knows to translate
            # 5000 chars per source = enough for faculty lists, programs, etc.
            context_parts.append(
                f"[Source {i}] {result['title']} (Language: {result['language']})\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content'][:5000]}...\n"
            )
        
        return "\n\n".join(context_parts)
