"""
Import test documents into CODEX database

This script imports the test legal documents into the database
with embeddings for RAG functionality.
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, '/app')

from services.rag.load_documents import DocumentLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


async def main():
    """Import test documents."""
    
    # Database connection
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/codex_db')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_key_here')
    
    print("=" * 60)
    print("CODEX Document Import Script")
    print("=" * 60)
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print(f"OpenAI Key: {'SET' if OPENAI_API_KEY and OPENAI_API_KEY != 'your_key_here' else 'NOT SET'}")
    print("=" * 60)
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == 'your_key_here':
        print("\n⚠️  WARNING: OpenAI API key not configured!")
        print("Set OPENAI_API_KEY in .env file to enable embeddings.")
        print("\nContinuing anyway (will fail at embedding step)...\n")
    
    # Initialize loader
    loader = DocumentLoader(
        db_url=DATABASE_URL,
        openai_api_key=OPENAI_API_KEY,
        chunk_size=500,
        chunk_overlap=50
    )
    
    # Documents to import
    documents = [
        {
            'path': '/app/test_documents/obciansky_zakonnik.txt',
            'metadata': {
                'document_type': 'legislation',
                'practice_area': 'civil',
                'jurisdiction': 'SK',
                'title': 'Občiansky zákonník SR - Výňatky'
            }
        },
        {
            'path': '/app/test_documents/zmluvy_prirucka.txt',
            'metadata': {
                'document_type': 'guide',
                'practice_area': 'civil',
                'jurisdiction': 'SK',
                'title': 'Zmluvy v slovenskom práve - Sprievodca'
            }
        },
        {
            'path': '/app/test_documents/nahrada_skody.txt',
            'metadata': {
                'document_type': 'guide',
                'practice_area': 'civil',
                'jurisdiction': 'SK',
                'title': 'Náhrada škody v slovenskom práve'
            }
        }
    ]
    
    # Import each document
    total_chunks = 0
    for doc in documents:
        print(f"\n📄 Processing: {doc['metadata']['title']}")
        print(f"   Path: {doc['path']}")
        
        try:
            chunks = await loader.load_from_file(
                file_path=doc['path'],
                metadata=doc['metadata']
            )
            total_chunks += chunks
            print(f"   ✅ Imported {chunks} chunks")
        except FileNotFoundError:
            print(f"   ❌ File not found: {doc['path']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✨ Import complete! Total chunks: {total_chunks}")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
