-- Migration: Add Educational Platform Tables
-- Date: 2026-01-10
-- Purpose: Transform CODEX legal platform to Student educational platform

-- ============================================
-- UNIVERSITIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS universities (
    id SERIAL PRIMARY KEY,
    jurisdiction_id INTEGER REFERENCES jurisdictions(id),
    name VARCHAR(500) NOT NULL,
    name_local VARCHAR(500),
    type VARCHAR(50) DEFAULT 'university', -- university, vocational, language_school
    website_url VARCHAR(500),
    logo_url VARCHAR(500),
    city VARCHAR(100),
    country VARCHAR(2) DEFAULT 'SK',
    description TEXT,
    data_container_path VARCHAR(500), -- Path to scraped data in MinIO
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT,
    ranking_position INTEGER,
    student_count INTEGER,
    last_updated TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_universities_jurisdiction ON universities(jurisdiction_id);
CREATE INDEX idx_universities_country ON universities(country);
CREATE INDEX idx_universities_type ON universities(type);

-- ============================================
-- PROGRAMS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS programs (
    id SERIAL PRIMARY KEY,
    university_id INTEGER REFERENCES universities(id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL,
    name_local VARCHAR(500),
    degree_level VARCHAR(50) NOT NULL, -- bachelor, master, phd, vocational, language_course
    field_of_study VARCHAR(200),
    language VARCHAR(10) DEFAULT 'sk',
    duration_years DECIMAL(3,1),
    duration_months INTEGER,
    tuition_fee INTEGER DEFAULT 0, -- in EUR cents (0 = free)
    description TEXT,
    admission_requirements JSON, -- Structured requirements
    application_deadline DATE,
    start_date DATE,
    capacity INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_programs_university ON programs(university_id);
CREATE INDEX idx_programs_degree_level ON programs(degree_level);
CREATE INDEX idx_programs_field ON programs(field_of_study);

-- ============================================
-- STUDENT PROFILES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS student_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Academic Information
    current_education_level VARCHAR(50), -- high_school, bachelor, master
    gpa DECIMAL(3,2),
    graduation_year INTEGER,
    field_of_interest VARCHAR(200),
    
    -- Language Proficiency (JSON: {"en": "C1", "de": "B2", "sk": "native"})
    language_proficiency JSON,
    
    -- Achievements and Experience
    achievements TEXT[],
    extracurricular TEXT[],
    work_experience TEXT,
    
    -- Documents (JSON array of document IDs or paths)
    documents JSON,
    
    -- Preferences
    preferred_countries VARCHAR(10)[], -- ["SK", "CZ", "PL"]
    preferred_degree_level VARCHAR(50),
    budget_max INTEGER, -- in EUR cents
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_student_profiles_user ON student_profiles(user_id);

-- ============================================
-- APPLICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    program_id INTEGER REFERENCES programs(id) ON DELETE CASCADE,
    
    -- Application Status
    status VARCHAR(50) DEFAULT 'draft', -- draft, submitted, under_review, accepted, rejected, withdrawn
    
    -- Documents (JSON: {"transcript": "path", "motivation_letter": "path", ...})
    documents JSON,
    
    -- AI Assistance
    ai_guidance JSON, -- AI-generated step-by-step guidance
    ai_chat_history JSON, -- Chat history with AI assistant
    probability_score INTEGER, -- 0-100 admission probability
    
    -- Important Dates
    submitted_at TIMESTAMP,
    reviewed_at TIMESTAMP,
    decision_date TIMESTAMP,
    
    -- Notes
    student_notes TEXT,
    admin_notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_program ON applications(program_id);
CREATE INDEX idx_applications_status ON applications(status);

-- ============================================
-- UNIVERSITY CHAT SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS university_chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    university_id INTEGER REFERENCES universities(id) ON DELETE CASCADE,
    program_id INTEGER REFERENCES programs(id) ON DELETE SET NULL,
    
    -- Chat Data
    messages JSON, -- Array of {role, content, timestamp}
    context JSON, -- University data context used
    
    -- Session Info
    session_started TIMESTAMP DEFAULT NOW(),
    session_ended TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_sessions_user ON university_chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_university ON university_chat_sessions(university_id);

-- ============================================
-- SAMPLE DATA: Slovak Universities (MVP)
-- ============================================

-- Insert sample Slovak universities
INSERT INTO universities (jurisdiction_id, name, name_local, type, website_url, city, country, description) VALUES
(
    (SELECT id FROM jurisdictions WHERE code = 'SK' LIMIT 1),
    'Comenius University in Bratislava',
    'Univerzita Komenského v Bratislave',
    'university',
    'https://uniba.sk',
    'Bratislava',
    'SK',
    'The oldest and largest university in Slovakia, founded in 1919.'
),
(
    (SELECT id FROM jurisdictions WHERE code = 'SK' LIMIT 1),
    'Slovak University of Technology in Bratislava',
    'Slovenská technická univerzita v Bratislave',
    'university',
    'https://www.stuba.sk',
    'Bratislava',
    'SK',
    'Leading technical university in Slovakia, specializing in engineering and technology.'
),
(
    (SELECT id FROM jurisdictions WHERE code = 'SK' LIMIT 1),
    'University of Economics in Bratislava',
    'Ekonomická univerzita v Bratislave',
    'university',
    'https://euba.sk',
    'Bratislava',
    'SK',
    'Premier economics and business university in Slovakia.'
),
(
    (SELECT id FROM jurisdictions WHERE code = 'SK' LIMIT 1),
    'Pavol Jozef Šafárik University in Košice',
    'Univerzita Pavla Jozefa Šafárika v Košiciach',
    'university',
    'https://www.upjs.sk',
    'Košice',
    'SK',
    'Major university in eastern Slovakia, strong in natural sciences and medicine.'
),
(
    (SELECT id FROM jurisdictions WHERE code = 'SK' LIMIT 1),
    'Technical University of Košice',
    'Technická univerzita v Košiciach',
    'university',
    'https://www.tuke.sk',
    'Košice',
    'SK',
    'Technical university focused on engineering, informatics, and technology.'
);

-- ============================================
-- NOTES
-- ============================================
-- This migration creates the foundation for the educational platform
-- Next steps:
-- 1. Add programs for each university
-- 2. Populate admission requirements
-- 3. Update AI agents to work with this data
-- 4. Create frontend to display universities
