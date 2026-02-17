-- Copy working password hash from regular user to admin accounts
-- This sets admin password to same as karpaty88888@post.sk user
UPDATE users 
SET hashed_password = '$pbkdf2-sha256$29000$.9.bE0Ko1VqLkZJy7n0vhQ$OhkbzU1/f1KHiaWvMEADTCI8jKNs7.3NJPHgDn0UeZ0'
WHERE role = 'admin';

-- Verify update
SELECT id, email, role, LEFT(hashed_password, 20) as hash_preview, LENGTH(hashed_password) as hash_len
FROM users 
WHERE role = 'admin';
