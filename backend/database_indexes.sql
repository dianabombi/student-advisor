-- CODEX Database Setup: pgvector indexes for RAG performance
-- Run this after backend creates the tables

-- 1. Verify pgvector extension is installed
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create IVFFlat index for fast similarity search on document_chunks
-- IVFFlat divides vectors into lists for faster approximate nearest neighbor search
-- lists = 100 is good for up to 1M vectors (adjust based on dataset size)
CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx 
ON document_chunks 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Alternative: Use HNSW index (more accurate but slower to build)
-- Uncomment if you prefer accuracy over build time:
-- CREATE INDEX IF NOT EXISTS document_chunks_embedding_hnsw_idx 
-- ON document_chunks 
-- USING hnsw (embedding vector_cosine_ops);

-- 3. Create indexes on foreign keys for join performance
CREATE INDEX IF NOT EXISTS document_chunks_document_id_idx 
ON document_chunks(document_id);

CREATE INDEX IF NOT EXISTS chat_messages_session_id_idx 
ON chat_messages(session_id);

CREATE INDEX IF NOT EXISTS chat_messages_user_id_idx 
ON chat_messages(user_id);

CREATE INDEX IF NOT EXISTS chat_sessions_user_id_idx 
ON chat_sessions(user_id);

-- 4. Create index on updated_at for session sorting
CREATE INDEX IF NOT EXISTS chat_sessions_updated_at_idx 
ON chat_sessions(updated_at DESC);

-- 5. Verify indexes were created
SELECT 
    tablename, 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
  AND (tablename LIKE '%chunk%' OR tablename LIKE '%chat%')
ORDER BY tablename, indexname;
