# RAG Retrieval Chain - Usage Examples

## Quick Start

### Basic Usage

```python
from services.rag.retrieval_chain import RetrievalChain
from sqlalchemy.orm import Session

# Initialize chain
chain = RetrievalChain(db=db_session)

# Ask a question
result = await chain.query(
    question="Aké sú podmienky platnosti zmluvy?",
    k=3
)

print(result['answer'])
print(result['sources'])
```

### Step-by-Step Usage

```python
from services.rag.retrieval_chain import retrieve_context, generate_answer

# Step 1: Retrieve relevant context
chunks = await retrieve_context(
    query="Aké sú podmienky platnosti zmluvy?",
    k=3,
    db=db_session
)

# Step 2: Generate answer
answer = await generate_answer(
    query="Aké sú podmienky platnosti zmluvy?",
    context_text=chunks,
    db=db_session
)

print(answer)
```

## Advanced Usage

### With Filters

```python
# Filter by practice area
result = await chain.query(
    question="Aké sú podmienky platnosti zmluvy?",
    k=5,
    filters={'practice_area': 'civil', 'jurisdiction': 'SK'}
)
```

### Custom Prompt Template

```python
custom_prompt = """Na základe nasledujúceho kontextu:

{context}

Odpovedz stručne a jasne na otázku: {question}

Odpoveď:"""

chain.set_prompt_template(custom_prompt)

result = await chain.query("Čo je zmluva?", k=3)
```

### Adjust Temperature

```python
# More creative responses
chain.set_temperature(0.7)

# Deterministic responses (default)
chain.set_temperature(0.0)
```

## Integration with FastAPI

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.rag.retrieval_chain import RetrievalChain

router = APIRouter()

@router.post("/api/rag/query")
async def rag_query(
    question: str,
    practice_area: str = None,
    db: Session = Depends(get_db)
):
    chain = RetrievalChain(db=db)
    
    filters = {}
    if practice_area:
        filters['practice_area'] = practice_area
    
    result = await chain.query(
        question=question,
        k=5,
        filters=filters
    )
    
    return result
```

## Testing

```python
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.rag.retrieval_chain import RetrievalChain

# Setup database
DATABASE_URL = "postgresql://user:password@localhost:5433/codex_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async def test_rag():
    db = SessionLocal()
    chain = RetrievalChain(db=db)
    
    # Test questions
    questions = [
        "Aké sú podmienky platnosti zmluvy?",
        "Kedy sa zmluva stáva neplatnou?",
        "Čo je náhrada škody?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        result = await chain.query(question, k=3)
        print(f"A: {result['answer']}")
        print(f"Sources: {len(result['sources'])}")
    
    db.close()

# Run test
asyncio.run(test_rag())
```

## Response Format

```python
{
    'answer': 'Zmluva je platná, ak spĺňa všetky zákonné náležitosti...',
    'sources': [
        {
            'filename': 'obciansky_zakonnik.txt',
            'chunk_index': 5,
            'distance': 0.234
        },
        {
            'filename': 'zmluvy_prirucka.pdf',
            'chunk_index': 12,
            'distance': 0.289
        }
    ],
    'context': '[Optional] Raw context text...'
}
```

## Key Functions

### `retrieve_context(query, k, db, filters)`
- Computes query embedding via `OpenAIEmbeddings().embed_query()`
- Executes SQL query with L2 distance: `embedding <-> query_embedding`
- Returns top k most relevant chunks

### `generate_answer(query, context_text, db)`
- Uses LangChain `LLMChain` with custom prompt
- Integrates retrieved context
- Returns formatted answer

### `RetrievalChain.query(question, k, filters)`
- Complete pipeline: retrieve → generate
- One-line RAG execution
- Returns answer with sources

## Performance Tips

1. **Optimal k value**: 3-5 chunks usually sufficient
2. **Use filters**: Narrow search by practice area
3. **Cache embeddings**: Reuse for similar queries
4. **Batch queries**: Process multiple questions together
5. **Monitor distance**: Lower = more relevant (< 0.5 is good)

## Troubleshooting

### "No relevant documents found"
- Check if documents are loaded: `SELECT COUNT(*) FROM document_chunks`
- Verify embeddings exist: `SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL`

### "OpenAI API error"
- Verify API key in `.env`
- Check API credits/quota
- Ensure network connectivity

### "Slow retrieval"
- Verify indexes exist: `\di document_chunks_embedding_idx`
- Consider reducing k value
- Use filters to narrow search
