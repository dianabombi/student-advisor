"""
Load Legal Documents into RAG System

Organizes and loads legal documents from legal_docs/ into the database
with proper practice area categorization for RAG retrieval.
"""

import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from main import SessionLocal, engine
from services.rag.simple_loader import SimpleDocumentLoader


def load_all_legal_documents():
    """Load all legal documents organized by practice area."""
    
    print("🚀 Starting legal documents import...")
    print("=" * 60)
    
    # Initialize services
    db = SessionLocal()
    loader = SimpleDocumentLoader(db, chunk_size=1000)
    
    # Define documents by practice area
    documents = {
        'civil': [
            'legal_docs/civil/obciansky_zakonnik.txt',
            'legal_docs/civil/zmluvy_prirucka.txt',
            'legal_docs/civil/nahrada_skody.txt',
        ],
        'labor': [
            # Add labor law documents here when available
        ],
        'commercial': [
            # Add commercial law documents here when available
        ],
        'family': [
            # Add family law documents here when available
        ]
    }
    
    total_loaded = 0
    total_chunks = 0
    
    try:
        for practice_area, file_paths in documents.items():
            if not file_paths:
                print(f"\n⏭️  Skipping {practice_area} - no documents")
                continue
                
            print(f"\n📚 Loading {practice_area.upper()} law documents...")
            print("-" * 60)
            
            for file_path in file_paths:
                full_path = os.path.join(os.path.dirname(__file__), file_path)
                
                if not os.path.exists(full_path):
                    print(f"  ⚠️  File not found: {file_path}")
                    continue
                
                try:
                    print(f"  📄 Processing: {os.path.basename(file_path)}")
                    
                    # Load document
                    doc_id, chunks_count = loader.load_document(
                        file_path=full_path,
                        practice_area=practice_area,
                        document_type='law',
                        jurisdiction='SK'
                    )
                    
                    total_loaded += 1
                    total_chunks += chunks_count
                    
                    print(f"     ✅ Loaded: {chunks_count} chunks")
                    
                except Exception as e:
                    print(f"     ❌ Error: {str(e)}")
                    continue
        
        # Summary
        print("\n" + "=" * 60)
        print(f"✅ Import Complete!")
        print(f"   Documents loaded: {total_loaded}")
        print(f"   Total chunks: {total_chunks}")
        print("=" * 60)
        
        # Verify database
        docs_count = db.execute(text("SELECT COUNT(*) FROM documents")).scalar()
        chunks_count = db.execute(text("SELECT COUNT(*) FROM document_chunks")).scalar()
        
        print(f"\n📊 Database Status:")
        print(f"   Documents in DB: {docs_count}")
        print(f"   Chunks in DB: {chunks_count}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CODEX Legal Documents Importer")
    print("=" * 60)
    
    # Check if embeddings will work
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "your_key_here":
        print("\n⚠️  WARNING: No valid OPENAI_API_KEY found!")
        print("   Embeddings will be zero vectors (fallback mode)")
        print("   RAG will NOT work properly without real embeddings")
        print("\n   To fix: Set OPENAI_API_KEY in .env file")
        print("\n   Continuing with fallback mode...")
    
    load_all_legal_documents()
