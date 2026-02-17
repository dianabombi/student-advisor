-- Reset admin passwords to 'admin123'
UPDATE users 
SET hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr3MNiYyS'
WHERE email IN ('valo-sro@centrum.sk', 'Eduard.pavlyshche@gmail.com') 
AND role = 'admin';

-- Verify update
SELECT id, email, role, LENGTH(hashed_password) as hash_length 
FROM users 
WHERE role = 'admin';
