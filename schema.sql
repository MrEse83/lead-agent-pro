-- Lead Agent Pro — Database Schema
-- Multi-industry outreach platform
-- Run once against your Neon database:
-- psql $DATABASE_URL -f schema.sql

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,

    -- Basic info from scraper
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(100),
    website VARCHAR(500),
    google_maps_url VARCHAR(1000),
    category VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'United States',
    source VARCHAR(100),
    rating DECIMAL(2,1),

    -- Enrichment results
    email VARCHAR(255),
    whatsapp_number VARCHAR(100),
    has_whatsapp BOOLEAN DEFAULT FALSE,
    has_booking_form BOOLEAN DEFAULT FALSE,
    has_chatbot BOOLEAN DEFAULT FALSE,
    has_contact_form BOOLEAN DEFAULT FALSE,
    instagram_handle VARCHAR(255),
    instagram_followers INTEGER,
    runs_ads BOOLEAN DEFAULT FALSE,
    instagram_checked_at TIMESTAMP,
    enrichment_status VARCHAR(50) DEFAULT 'pending',
    enrichment_error TEXT,
    enriched_at TIMESTAMP,

    -- AI analysis results
    ai_summary TEXT,
    automation_score INTEGER,
    score_reason TEXT,
    analysis_status VARCHAR(50) DEFAULT 'pending',
    analyzed_at TIMESTAMP,

    -- Lead qualification
    lead_status VARCHAR(50) DEFAULT 'new',
    priority VARCHAR(20),

    -- Outreach
    outreach_email TEXT,
    outreach_whatsapp TEXT,
    outreach_generated_at TIMESTAMP,
    contacted_at TIMESTAMP,
    contact_channel VARCHAR(50),
    notes TEXT,

    -- Timestamps
    discovered_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(name, address)
);

CREATE INDEX IF NOT EXISTS idx_lead_status ON leads(lead_status);
CREATE INDEX IF NOT EXISTS idx_automation_score ON leads(automation_score DESC);
CREATE INDEX IF NOT EXISTS idx_city ON leads(city);
CREATE INDEX IF NOT EXISTS idx_category ON leads(category);
CREATE INDEX IF NOT EXISTS idx_country ON leads(country);
CREATE INDEX IF NOT EXISTS idx_enrichment_status ON leads(enrichment_status);
CREATE INDEX IF NOT EXISTS idx_analysis_status ON leads(analysis_status);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON leads;
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON leads
FOR EACH ROW EXECUTE FUNCTION update_updated_at();