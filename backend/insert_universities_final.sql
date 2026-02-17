-- Set client encoding to UTF8
SET client_encoding = 'UTF8';

-- Delete existing universities
DELETE FROM universities WHERE id IN (1,2,3,4,5);

-- Insert with proper UTF-8 characters
INSERT INTO universities (id, name, name_local, type, city, country, description, website_url, student_count, ranking_position, jurisdiction_id, is_active)
VALUES 
(1, 'Comenius University in Bratislava', 'Univerzita Komenského v Bratislave', 'university', 'Bratislava', 'SK', 
 'Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919.', 'https://uniba.sk', 20000, 1, 1, TRUE),

(2, 'Slovak University of Technology in Bratislava', 'Slovenská technická univerzita v Bratislave', 'university', 'Bratislava', 'SK',
 'Popredná technická univerzita zameraná na inžinierstvo a technológie.', 'https://stuba.sk', 15000, 2, 1, TRUE),

(3, 'University of Economics in Bratislava', 'Ekonomická univerzita v Bratislave', 'university', 'Bratislava', 'SK',
 'Špecializovaná univerzita pre ekonomiku, obchod a manažment.', 'https://euba.sk', 8000, 3, 1, TRUE),

(4, 'Pavol Jozef Šafárik University in Košice', 'Univerzita Pavla Jozefa Šafárika v Košiciach', 'university', 'Košice', 'SK',
 'Významná univerzita vo východnom Slovensku s dlhou tradíciou.', 'https://upjs.sk', 7000, 4, 1, TRUE),

(5, 'Matej Bel University in Banská Bystrica', 'Univerzita Mateja Bela v Banskej Bystrici', 'university', 'Banská Bystrica', 'SK',
 'Moderná univerzita v strednom Slovensku s širokým spektrom programov.', 'https://umb.sk', 9000, 5, 1, TRUE);
