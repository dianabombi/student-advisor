# RAG Module for CODEX Legal Platform

## Overview

This module implements Retrieval-Augmented Generation (RAG) for intelligent legal document analysis and consultation.

## Structure

```
rag/
├── __init__.py          # Package exports
├── embeddings.py        # Text embedding generation
├── retriever.py         # Vector similarity search
└── chain.py             # Complete RAG pipeline
```

## Components

### 1. EmbeddingService (`embeddings.py`)
- Generates text embeddings using OpenAI API
- Supports batch processing
- Includes caching for frequently used queries
- Fallback to zero vectors when API unavailable

### 2. DocumentRetriever (`retriever.py`)
- Vector similarity search using pgvector
- Metadata filtering (practice area, jurisdiction, document type)
- Context retrieval (surrounding chunks)
- Configurable result count

### 3. RAGChain (`chain.py`)
- Complete RAG pipeline: Query → Retrieve → Generate
- Automatic query embedding
- Context construction from retrieved chunks
- AI response generation with OpenAI
- Source attribution

## Usage Example

```python
from services.rag import EmbeddingService, DocumentRetriever, RAGChain
from sqlalchemy.orm import Session

# Initialize services
embedding_service = EmbeddingService()
retriever = DocumentRetriever(db=db_session, top_k=5)
rag_chain = RAGChain(
    embedding_service=embedding_service,
    retriever=retriever,
    model="gpt-4"
)

# Execute RAG query
result = await rag_chain.query(
    question="Aké sú podmienky platnosti zmluvy?",
    filters={'practice_area': 'civil'},
    top_k=5,
    include_sources=True
)

print(result['answer'])
print(result['sources'])
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key for embeddings and generation

### Models
- **Embedding**: `text-embedding-3-small` (1536 dimensions)
- **Generation**: `gpt-4` (configurable)

## Features

✅ **Semantic Search** - Find relevant document sections using vector similarity  
✅ **Context-Aware** - AI responses informed by actual document content  
✅ **Source Attribution** - Shows which documents informed the answer  
✅ **Flexible Filtering** - Filter by practice area, jurisdiction, document type  
✅ **Batch Processing** - Efficient embedding generation  
✅ **Caching** - Reduces API calls for repeated queries  
✅ **Fallback Handling** - Graceful degradation when API unavailable  

## Integration with Main API

The RAG module is integrated into the main FastAPI application via the chat endpoint:

```python
from services.rag import EmbeddingService, DocumentRetriever, RAGChain

# In chat endpoint
embedding_service = EmbeddingService()
retriever = DocumentRetriever(db, top_k=5)
rag_chain = RAGChain(embedding_service, retriever)

result = await rag_chain.query(
    question=request.message,
    filters={'practice_area': user_practice_area}
)
```

## Performance

- **Embedding generation**: ~1-2 seconds per document
- **Similarity search**: <500ms with IVFFlat index
- **End-to-end RAG**: 3-5 seconds (depends on OpenAI API)

## Future Enhancements

- [ ] Support for multiple embedding models
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking of retrieved chunks
- [ ] Conversation memory
- [ ] Custom prompts per practice area
