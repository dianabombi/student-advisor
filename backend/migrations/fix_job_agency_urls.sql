-- Fix Job Agency URLs - Remove subpages, use only main domains
-- Run this in pgAdmin, DBeaver, or psql

-- 1. Update Profesia.sk URLs
UPDATE job_agencies 
SET website_url = 'https://www.profesia.sk'
WHERE website_url LIKE '%profesia.sk%'
AND website_url != 'https://www.profesia.sk';

-- 2. Update StudentJob URLs
UPDATE job_agencies 
SET website_url = 'https://www.studentjob.sk'
WHERE website_url LIKE '%studentjob.sk%'
AND website_url != 'https://www.studentjob.sk';

-- 3. Update Brigada.sk URLs
UPDATE job_agencies 
SET website_url = 'https://www.brigada.sk'
WHERE website_url LIKE '%brigada.sk%'
AND website_url != 'https://www.brigada.sk';

-- 4. Update Kariera.sk URLs (including kariera.zoznam.sk)
UPDATE job_agencies 
SET website_url = 'https://www.kariera.sk'
WHERE (website_url LIKE '%kariera.sk%' OR website_url LIKE '%kariera.zoznam.sk%')
AND website_url != 'https://www.kariera.sk';

-- 5. Update Indeed URLs
UPDATE job_agencies 
SET website_url = 'https://sk.indeed.com'
WHERE (website_url LIKE '%indeed.com%' OR website_url LIKE '%indeed.sk%')
AND website_url != 'https://sk.indeed.com';

-- 6. Update Manpower URLs
UPDATE job_agencies 
SET website_url = 'https://www.manpower.sk'
WHERE website_url LIKE '%manpower.sk%'
AND website_url != 'https://www.manpower.sk';

-- 7. Update Grafton URLs
UPDATE job_agencies 
SET website_url = 'https://www.grafton.sk'
WHERE website_url LIKE '%grafton.sk%'
AND website_url != 'https://www.grafton.sk';

-- Verify changes
SELECT name, city, website_url 
FROM job_agencies 
ORDER BY city, name;
