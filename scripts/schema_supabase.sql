-- ==============================================================================
-- Supabase Schema Migration: Accessibility Dashboard History
-- Target Project: https://frkbjkugjfbvufsszxjm.supabase.co
-- Run this script in: Supabase Dashboard -> SQL Editor -> New Query -> Run
-- ==============================================================================

-- 1. Create analyses table
CREATE TABLE IF NOT EXISTS public.analyses (
    id BIGSERIAL PRIMARY KEY,
    timestamp TEXT NOT NULL,
    doc_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    input_text TEXT NOT NULL,
    accessibility_score DOUBLE PRECISION NOT NULL,
    readability_score DOUBLE PRECISION NOT NULL,
    grade_level DOUBLE PRECISION NOT NULL,
    reading_time DOUBLE PRECISION NOT NULL,
    violations_count INTEGER NOT NULL,
    issues_json TEXT NOT NULL,
    metrics_json TEXT NOT NULL,
    simplified_text TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create indexes for high-speed search and filtering
CREATE INDEX IF NOT EXISTS idx_analyses_timestamp ON public.analyses (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_doc_name ON public.analyses (doc_name);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS Policy granting full read/write access to authenticated and anonymous API clients
DROP POLICY IF EXISTS "Allow public access to analyses" ON public.analyses;
CREATE POLICY "Allow public access to analyses"
    ON public.analyses
    FOR ALL
    TO anon, authenticated
    USING (true)
    WITH CHECK (true);

-- 5. Verification query
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'analyses';
