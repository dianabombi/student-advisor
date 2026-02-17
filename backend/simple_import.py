"""
Simple document loader for importing test documents
"""
import os
import sys
sys.path.insert(0, '/app')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from openai import OpenAI


async def load_from_file(file_path, metadata, db_url, api_key):
    """Load a single file and create chunks with embeddings."""
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize OpenAI
    client = OpenAI(api_key=api_key)
    
    # Simple chunking (split by paragraphs)
    chunks = []
    current_chunk = ""
    for line in content.split('\n'):
        if len(current_chunk) + len(line) > 500:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            current_chunk += "\n" + line
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    print(f"Split into {len(chunks)} chunks")
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    
    # Database connection
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Insert document
        insert_doc = text("""
            INSERT INTO documents (filename, file_path, document_type, practice_area, jurisdiction, extracted_data, confidence, uploaded_at, user_id)
            VALUES (:filename, :file_path, :doc_type, :practice_area, :jurisdiction, :extracted_data, :confidence, :uploaded_at, :user_id)
            RETURNING id
        """)
        
        result = db.execute(insert_doc, {
            'filename': metadata.get('title', os.path.basename(file_path)),
            'file_path': file_path,
            'doc_type': metadata.get('document_type', 'guide'),
            'practice_area': metadata.get('practice_area', 'civil'),
            'jurisdiction': metadata.get('jurisdiction', 'SK'),
            'extracted_data': {'text': content[:1000]},
            'confidence': 100,
            'uploaded_at': datetime.utcnow(),
            'user_id': 1
        })
        
        document_id = result.fetchone()[0]
        print(f"Created document ID: {document_id}")
        
        # Insert chunks
        insert_chunk = text("""
            INSERT INTO document_chunks (document_id, chunk_index, content, embedding, chunk_metadata, created_at)
            VALUES (:doc_id, :idx, :content, :embedding, :metadata, :created_at)
        """)
        
        for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            db.execute(insert_chunk, {
                'doc_id': document_id,
                'idx': idx,
                'content': chunk_text,
                'embedding': embedding,
                'metadata': metadata,
                'created_at': datetime.utcnow()
            })
        
        db.commit()
        print(f"✅ Imported {len(chunks)} chunks")
        return len(chunks)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        return 0
    finally:
        db.close()


async def main():
    """Import test documents."""
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/codex_db')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_key_here')
    
    print("=" * 60)
    print("CODEX Document Import")
    print("=" * 60)
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == 'your_key_here':
        print("\n⚠️  OpenAI API key not configured!")
        print("Embeddings will fail without a valid key.\n")
        return
    
    documents = [
        {
            'path': '/app/test_documents/obciansky_zakonnik.txt',
            'metadata': {
                'title': 'Občiansky zákonník SR',
                'document_type': 'legislation',
                'practice_area': 'civil',
                'jurisdiction': 'SK'
            }
        },
        {
            'path': '/app/test_documents/zmluvy_prirucka.txt',
            'metadata': {
                'title': 'Zmluvy - Sprievodca',
                'document_type': 'guide',
                'practice_area': 'civil',
                'jurisdiction': 'SK'
            }
        },
        {
            'path': '/app/test_documents/nahrada_skody.txt',
            'metadata': {
                'title': 'Náhrada škody',
                'document_type': 'guide',
                'practice_area': 'civil',
                'jurisdiction': 'SK'
            }
        }
    ]
    
    total_chunks = 0
    for doc in documents:
        print(f"\n📄 {doc['metadata']['title']}")
        chunks = await load_from_file(doc['path'], doc['metadata'], DATABASE_URL, OPENAI_API_KEY)
        total_chunks += chunks
    
    print("\n" + "=" * 60)
    print(f"✨ Total chunks imported: {total_chunks}")
    print("=" * 60)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
