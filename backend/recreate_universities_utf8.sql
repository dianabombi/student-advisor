-- Delete existing universities
DELETE FROM universities WHERE id IN (1,2,3,4,5);

-- Insert with proper UTF-8 using E'' escape syntax
INSERT INTO universities (id, name, name_local, type, city, country, description, website_url, student_count, ranking_position, jurisdiction_id)
VALUES 
(1, 'Comenius University in Bratislava', E'Univerzita Komenského v Bratislave', 'university', 'Bratislava', 'SK', 
 E'Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919.', 'https://uniba.sk', 20000, 1, 1),

(2, 'Slovak University of Technology in Bratislava', E'Slovenská technická univerzita v Bratislave', 'university', 'Bratislava', 'SK',
 E'Popredná technická univerzita zameraná na inžinierstvo a technológie.', 'https://stuba.sk', 15000, 2, 1),

(3, 'University of Economics in Bratislava', E'Ekonomická univerzita v Bratislave', 'university', 'Bratislava', 'SK',
 E'Špecializovaná univerzita pre ekonomiku, obchod a manažment.', 'https://euba.sk', 8000, 3, 1),

(4, E'Pavol Jozef Šafárik University in Košice', E'Univerzita Pavla Jozefa Šafárika v Košiciach', 'university', E'Košice', 'SK',
 E'Významná univerzita vo východnom Slovensku s dlhou tradíciou.', 'https://upjs.sk', 7000, 4, 1),

(5, E'Matej Bel University in Banská Bystrica', E'Univerzita Mateja Bela v Banskej Bystrici', 'university', E'Banská Bystrica', 'SK',
 E'Moderná univerzita v strednom Slovensku s širokým spektrom programov.', 'https://umb.sk', 9000, 5, 1);
