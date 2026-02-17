-- RAG Database Schema for University Content and Embeddings
-- Supports all educational institutions across all jurisdictions

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: university_content
-- Stores scraped content from university websites
CREATE TABLE IF NOT EXISTS university_content (
    id SERIAL PRIMARY KEY,
    university_id INTEGER NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    content_type VARCHAR(50), -- 'admission', 'programs', 'fees', 'contact', 'general', 'scholarships'
    language VARCHAR(10), -- 'sk', 'cs', 'en', 'uk', 'pl', 'de', 'fr', 'es', 'it', 'ru'
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(university_id, url)
);

-- Table: university_embeddings
-- Stores vector embeddings for semantic search
CREATE TABLE IF NOT EXISTS university_embeddings (
    id SERIAL PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES university_content(id) ON DELETE CASCADE,
    embedding vector(1536), -- OpenAI text-embedding-ada-002 dimension
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(content_id)
);

-- Table: university_scraping_status
-- Tracks scraping status for each university
CREATE TABLE IF NOT EXISTS university_scraping_status (
    id SERIAL PRIMARY KEY,
    university_id INTEGER NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    last_scraped_at TIMESTAMP,
    scraping_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed'
    error_message TEXT,
    pages_scraped INTEGER DEFAULT 0,
    embeddings_generated INTEGER DEFAULT 0,
    next_scrape_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(university_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_university_content_university_id ON university_content(university_id);
CREATE INDEX IF NOT EXISTS idx_university_content_language ON university_content(language);
CREATE INDEX IF NOT EXISTS idx_university_content_type ON university_content(content_type);
CREATE INDEX IF NOT EXISTS idx_university_content_active ON university_content(is_active);

-- Vector similarity search index (IVFFlat for better performance)
CREATE INDEX IF NOT EXISTS idx_university_embeddings_vector 
ON university_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for scraping status
CREATE INDEX IF NOT EXISTS idx_scraping_status_university_id ON university_scraping_status(university_id);
CREATE INDEX IF NOT EXISTS idx_scraping_status_status ON university_scraping_status(scraping_status);

-- Function: Auto-create scraping status when new university is added
CREATE OR REPLACE FUNCTION create_scraping_status_for_new_university()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO university_scraping_status (university_id, scraping_status, next_scrape_at)
    VALUES (NEW.id, 'pending', NOW())
    ON CONFLICT (university_id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Automatically create scraping status for new universities
DROP TRIGGER IF EXISTS trigger_create_scraping_status ON universities;
CREATE TRIGGER trigger_create_scraping_status
AFTER INSERT ON universities
FOR EACH ROW
EXECUTE FUNCTION create_scraping_status_for_new_university();

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update updated_at for university_content
DROP TRIGGER IF EXISTS trigger_update_content_timestamp ON university_content;
CREATE TRIGGER trigger_update_content_timestamp
BEFORE UPDATE ON university_content
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Auto-update updated_at for university_scraping_status
DROP TRIGGER IF EXISTS trigger_update_scraping_status_timestamp ON university_scraping_status;
CREATE TRIGGER trigger_update_scraping_status_timestamp
BEFORE UPDATE ON university_scraping_status
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- View: University RAG readiness status
CREATE OR REPLACE VIEW university_rag_status AS
SELECT 
    u.id,
    u.name,
    u.jurisdiction_code,
    u.type,
    uss.scraping_status,
    uss.last_scraped_at,
    uss.pages_scraped,
    uss.embeddings_generated,
    uss.next_scrape_at,
    CASE 
        WHEN uss.embeddings_generated > 0 THEN TRUE 
        ELSE FALSE 
    END as rag_ready
FROM universities u
LEFT JOIN university_scraping_status uss ON u.id = uss.university_id
WHERE u.is_active = TRUE;

COMMENT ON TABLE university_content IS 'Stores scraped content from university websites for RAG';
COMMENT ON TABLE university_embeddings IS 'Stores vector embeddings for semantic search';
COMMENT ON TABLE university_scraping_status IS 'Tracks scraping status and readiness for each university';
COMMENT ON VIEW university_rag_status IS 'Shows RAG readiness status for all universities';
