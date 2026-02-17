-- Quick script to add Slovak universities directly to database
-- Run this inside the database container

-- Add 5 Slovak universities
INSERT INTO universities (jurisdiction_id, name, name_local, type, website_url, city, country, description, student_count, ranking_position, is_active, created_at)
SELECT 
    j.id,
    'Comenius University in Bratislava',
    'Univerzita Komenského v Bratislave',
    'university',
    'https://uniba.sk',
    'Bratislava',
    'SK',
    'The oldest and largest university in Slovakia, founded in 1919.',
    20000,
    1,
    true,
    NOW()
FROM jurisdictions j WHERE j.code = 'SK'
UNION ALL
SELECT 
    j.id,
    'Slovak University of Technology in Bratislava',
    'Slovenská technická univerzita v Bratislave',
    'university',
    'https://www.stuba.sk',
    'Bratislava',
    'SK',
    'Leading technical university specializing in engineering and technology.',
    15000,
    2,
    true,
    NOW()
FROM jurisdictions j WHERE j.code = 'SK'
UNION ALL
SELECT 
    j.id,
    'University of Economics in Bratislava',
    'Ekonomická univerzita v Bratislave',
    'university',
    'https://euba.sk',
    'Bratislava',
    'SK',
    'Premier economics and business university in Slovakia.',
    8000,
    3,
    true,
    NOW()
FROM jurisdictions j WHERE j.code = 'SK'
UNION ALL
SELECT 
    j.id,
    'Pavol Jozef Šafárik University in Košice',
    'Univerzita Pavla Jozefa Šafárika v Košiciach',
    'university',
    'https://www.upjs.sk',
    'Košice',
    'SK',
    'Major university in eastern Slovakia, strong in natural sciences.',
    7000,
    4,
    true,
    NOW()
FROM jurisdictions j WHERE j.code = 'SK'
UNION ALL
SELECT 
    j.id,
    'Matej Bel University',
    'Univerzita Mateja Bela',
    'university',
    'https://www.umb.sk',
    'Banská Bystrica',
    'SK',
    'Public university in central Slovakia with diverse programs.',
    9000,
    5,
    true,
    NOW()
FROM jurisdictions j WHERE j.code = 'SK';
