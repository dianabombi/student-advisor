-- Auto-scraping trigger for new universities
-- This trigger automatically queues scraping when a new university is added

CREATE OR REPLACE FUNCTION trigger_auto_scrape_new_university()
RETURNS TRIGGER AS $$
BEGIN
    -- Only trigger if university has a website
    IF NEW.website_url IS NOT NULL AND NEW.website_url != '' THEN
        -- Insert scraping status as 'pending'
        INSERT INTO university_scraping_status (
            university_id,
            scraping_status,
            created_at,
            updated_at
        ) VALUES (
            NEW.id,
            'pending',
            NOW(),
            NOW()
        )
        ON CONFLICT (university_id) DO NOTHING;
        
        -- Log for monitoring
        RAISE NOTICE 'Auto-scraping queued for new university: % (ID: %)', NEW.name, NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger on universities table
DROP TRIGGER IF EXISTS auto_scrape_new_university ON universities;
CREATE TRIGGER auto_scrape_new_university
    AFTER INSERT ON universities
    FOR EACH ROW
    EXECUTE FUNCTION trigger_auto_scrape_new_university();

-- Also trigger on website_url update (if university didn't have website before)
CREATE OR REPLACE FUNCTION trigger_auto_scrape_on_website_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Trigger if website was added/changed
    IF (OLD.website_url IS NULL OR OLD.website_url = '') 
       AND (NEW.website_url IS NOT NULL AND NEW.website_url != '') THEN
        
        INSERT INTO university_scraping_status (
            university_id,
            scraping_status,
            created_at,
            updated_at
        ) VALUES (
            NEW.id,
            'pending',
            NOW(),
            NOW()
        )
        ON CONFLICT (university_id) 
        DO UPDATE SET 
            scraping_status = 'pending',
            updated_at = NOW();
        
        RAISE NOTICE 'Auto-scraping queued for university with new website: % (ID: %)', NEW.name, NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS auto_scrape_on_website_update ON universities;
CREATE TRIGGER auto_scrape_on_website_update
    AFTER UPDATE ON universities
    FOR EACH ROW
    EXECUTE FUNCTION trigger_auto_scrape_on_website_update();

COMMENT ON FUNCTION trigger_auto_scrape_new_university() IS 'Automatically queue scraping for newly added universities';
COMMENT ON FUNCTION trigger_auto_scrape_on_website_update() IS 'Automatically queue scraping when website is added to existing university';
