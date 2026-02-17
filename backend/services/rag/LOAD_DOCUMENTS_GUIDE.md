# Document Loader - Usage Guide

## Overview

`load_documents.py` is a script for importing legal documents into the CODEX RAG system. It supports loading from local filesystem or MinIO, automatically extracts text, generates embeddings, and stores everything in the database.

## Features

✅ **Multiple Sources**: Local files or MinIO object storage  
✅ **Format Support**: PDF, DOCX, DOC, TXT  
✅ **Automatic Text Extraction**: Uses PyPDF2 and python-docx  
✅ **Chunking**: Intelligent text splitting with overlap  
✅ **Embeddings**: OpenAI embeddings via LangChain  
✅ **Metadata**: Practice area, jurisdiction, document type  
✅ **Batch Processing**: Efficient embedding generation  

## Prerequisites

1. **OpenAI API Key**: Set in `.env` file
2. **Database**: PostgreSQL with pgvector running
3. **Dependencies**: Install via `pip install -r requirements.txt`

## Usage

### From Local Filesystem

```bash
# Load all documents from a directory
python -m services.rag.load_documents \
  --source local \
  --path /path/to/legal/documents \
  --practice-area civil \
  --jurisdiction SK

# Example with specific document type
python -m services.rag.load_documents \
  --source local \
  --path ./legal_docs/contracts \
  --practice-area civil \
  --document-type contract \
  --jurisdiction SK
```

### From MinIO

```bash
# Load from MinIO bucket
python -m services.rag.load_documents \
  --source minio \
  --bucket legal-documents \
  --practice-area criminal \
  --jurisdiction SK

# Load from specific prefix in bucket
python -m services.rag.load_documents \
  --source minio \
  --bucket legal-docs \
  --practice-area commercial \
  --jurisdiction CZ
```

### Using Docker

```bash
# Run inside backend container
docker exec -it codex-backend-1 python -m services.rag.load_documents \
  --source local \
  --path /app/legal_docs \
  --practice-area civil
```

## Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--source` | Yes | Document source (`local` or `minio`) | `local` |
| `--path` | For local | Local directory path | `/docs/legal` |
| `--bucket` | For minio | MinIO bucket name | `legal-docs` |
| `--practice-area` | No | Practice area code | `civil` |
| `--jurisdiction` | No | Jurisdiction code (default: SK) | `SK` |
| `--document-type` | No | Document type (default: legal_reference) | `contract` |

## Practice Areas

- `civil` - Civilné právo
- `criminal` - Trestné právo
- `commercial` - Obchodné právo
- `labor` - Pracovné právo
- `administrative` - Správne právo
- `real_estate` - Nehnuteľnosti

## Document Types

- `legal_reference` - Legal reference documents (laws, codes)
- `contract` - Contracts and agreements
- `lawsuit` - Lawsuits and legal proceedings
- `legal_opinion` - Legal opinions and analyses
- `court_decision` - Court decisions and rulings

## Example Workflow

### 1. Prepare Documents

Create a directory structure:
```
legal_docs/
├── civil/
│   ├── obciansky_zakonnik.pdf
│   ├── zmluva_template.docx
│   └── sudne_rozhodnutie.pdf
├── criminal/
│   ├── trestny_zakon.pdf
│   └── trestny_poriadok.pdf
└── commercial/
    ├── obchodny_zakonnik.pdf
    └── konkurz_zakon.pdf
```

### 2. Load Civil Law Documents

```bash
python -m services.rag.load_documents \
  --source local \
  --path ./legal_docs/civil \
  --practice-area civil \
  --jurisdiction SK
```

### 3. Verify Import

```sql
-- Check documents
SELECT id, filename, practice_area, jurisdiction 
FROM documents 
WHERE practice_area = 'civil';

-- Check chunks
SELECT COUNT(*) as chunk_count, document_id 
FROM document_chunks 
GROUP BY document_id;
```

## Output Example

```
🚀 Starting document import from local...
Configuration: {'practice_area': 'civil', 'jurisdiction': 'SK', 'document_type': 'legal_reference'}

Loading: obciansky_zakonnik.pdf
Created document record: ID=1
Split into 245 chunks
Generating embeddings...
✅ Stored 245 chunks for 'obciansky_zakonnik.pdf'

Loading: zmluva_template.docx
Created document record: ID=2
Split into 12 chunks
Generating embeddings...
✅ Stored 12 chunks for 'zmluva_template.docx'

==================================================
📊 Import Summary
==================================================
Total documents: 2
Successful: 2
Failed: 0
Total chunks created: 257
==================================================
```

## Troubleshooting

### Error: "OPENAI_API_KEY not configured"
**Solution**: Set your API key in `.env` file:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### Error: "Bucket does not exist"
**Solution**: Create the bucket in MinIO first:
```bash
docker exec -it codex-minio-1 mc mb /data/legal-docs
```

### Error: "Could not extract text from PDF"
**Solution**: Ensure PDF is not scanned image. Use OCR service for scanned documents.

### Error: "Database connection failed"
**Solution**: Check `DATABASE_URL` environment variable and ensure PostgreSQL is running.

## Performance Tips

1. **Batch Processing**: Load multiple documents in one run
2. **Chunk Size**: Adjust `chunk_size` parameter for better performance
3. **API Rate Limits**: OpenAI has rate limits; add delays for large batches
4. **Database Indexes**: Ensure indexes are created (see `database_indexes.sql`)

## Integration with Main API

Once documents are loaded, they're automatically available for RAG queries:

```python
# In chat endpoint
from services.rag import RAGChain, EmbeddingService, DocumentRetriever

embedding_service = EmbeddingService()
retriever = DocumentRetriever(db, top_k=5)
rag_chain = RAGChain(embedding_service, retriever)

result = await rag_chain.query(
    question="Aké sú podmienky platnosti zmluvy?",
    filters={'practice_area': 'civil'}
)
```

## Next Steps

After loading documents:
1. Test RAG queries via chat interface
2. Monitor embedding quality
3. Adjust chunk size if needed
4. Add more documents as needed
