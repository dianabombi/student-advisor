-- Fix UTF-8 encoding for Slovak universities
UPDATE universities SET 
    name_local = 'Univerzita Komenského v Bratislave',
    description = 'Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919.'
WHERE id = 1;

UPDATE universities SET 
    name_local = 'Slovenská technická univerzita v Bratislave',
    description = 'Popredná technická univerzita zameraná na inžinierstvo a technológie.'
WHERE id = 2;

UPDATE universities SET 
    name_local = 'Ekonomická univerzita v Bratislave',
    description = 'Špecializovaná univerzita pre ekonomiku, obchod a manažment.'
WHERE id = 3;

UPDATE universities SET 
    name_local = 'Univerzita Pavla Jozefa Šafárika v Košiciach',
    description = 'Významná univerzita vo východnom Slovensku s dlhou tradíciou.'
WHERE id = 4;

UPDATE universities SET 
    name_local = 'Univerzita Mateja Bela v Banskej Bystrici',
    description = 'Moderná univerzita v strednom Slovensku s širokým spektrom programov.'
WHERE id = 5;
