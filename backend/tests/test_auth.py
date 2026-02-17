"""
Unit tests for authentication module.

Tests password hashing, JWT token generation/decoding, and auth functions.
"""

import pytest
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

# Import functions to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
)

# Security configuration (should match main config)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestPasswordHashing:
    """Tests for password hashing and verification."""
    
    def test_hash_password(self):
        """Test that password hashing works correctly."""
        password = "mySecurePassword123!"
        hashed = get_password_hash(password)
        
        # Hash should be different from password
        assert hashed != password
        
        # Hash should be a string
        assert isinstance(hashed, str)
        
        # Hash should start with bcrypt prefix
        assert hashed.startswith("$2b$")
    
    def test_verify_correct_password(self):
        """Test that correct password verification works."""
        password = "mySecurePassword123!"
        hashed = get_password_hash(password)
        
        # Correct password should verify
        assert verify_password(password, hashed) is True
    
    def test_verify_incorrect_password(self):
        """Test that incorrect password fails verification."""
        password = "mySecurePassword123!"
        wrong_password = "wrongPassword456"
        hashed = get_password_hash(password)
        
        # Wrong password should not verify
        assert verify_password(wrong_password, hashed) is False
    
    def test_different_passwords_different_hashes(self):
        """Test that same password generates different hashes (salt)."""
        password = "myPassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
        
        # But both should verify the same password
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_empty_password(self):
        """Test hashing empty password."""
        password = ""
        hashed = get_password_hash(password)
        
        # Should still hash
        assert hashed != password
        assert verify_password(password, hashed) is True
    
    def test_long_password(self):
        """Test hashing very long password."""
        password = "a" * 1000  # Very long password
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_special_characters_password(self):
        """Test password with special characters."""
        password = "P@ssw0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True


class TestJWTTokens:
    """Tests for JWT token generation and decoding."""
    
    def test_create_access_token(self):
        """Test that JWT token is created correctly."""
        data = {"sub": 1, "email": "test@example.com", "role": "user"}
        token = create_access_token(data)
        
        # Token should be a string
        assert isinstance(token, str)
        
        # Token should have 3 parts (header.payload.signature)
        assert len(token.split('.')) == 3
    
    def test_decode_valid_token(self):
        """Test decoding a valid JWT token."""
        user_id = 123
        email = "test@example.com"
        role = "admin"
        
        data = {"sub": user_id, "email": email, "role": role}
        token = create_access_token(data)
        
        # Decode token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verify data
        assert decoded["sub"] == user_id
        assert decoded["email"] == email
        assert decoded["role"] == role
        assert "exp" in decoded  # Expiration should be set
        assert "iat" in decoded  # Issued at should be set
    
    def test_token_expiration(self):
        """Test that token expiration is set correctly."""
        data = {"sub": 1}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check expiration is approximately 15 minutes from now
        exp_time = datetime.fromtimestamp(decoded["exp"])
        now = datetime.utcnow()
        time_diff = (exp_time - now).total_seconds()
        
        # Should be close to 15 minutes (900 seconds), allow 5 second margin
        assert 895 < time_diff < 905
    
    def test_default_token_expiration(self):
        """Test token with default expiration (30 minutes)."""
        data = {"sub": 1}
        token = create_access_token(data)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check expiration is approximately 30 minutes from now
        exp_time = datetime.fromtimestamp(decoded["exp"])
        now = datetime.utcnow()
        time_diff = (exp_time - now).total_seconds()
        
        # Should be close to 30 minutes (1800 seconds), allow 5 second margin
        assert 1795 < time_diff < 1805
    
    def test_decode_invalid_token(self):
        """Test that invalid token raises error."""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(JWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    def test_decode_with_wrong_secret(self):
        """Test that token with wrong secret fails."""
        data = {"sub": 1}
        token = create_access_token(data)
        
        wrong_secret = "wrong-secret-key"
        
        with pytest.raises(JWTError):
            jwt.decode(token, wrong_secret, algorithms=[ALGORITHM])
    
    def test_expired_token(self):
        """Test that expired token is rejected."""
        data = {"sub": 1}
        # Create token that expired 1 hour ago
        expires_delta = timedelta(hours=-1)
        token = create_access_token(data, expires_delta)
        
        with pytest.raises(JWTError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    def test_token_with_role(self):
        """Test token includes role information."""
        data = {
            "sub": 1,
            "email": "admin@example.com",
            "role": "admin",
            "is_verified": True
        }
        token = create_access_token(data)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert decoded["role"] == "admin"
        assert decoded["is_verified"] is True
    
    def test_token_immutability(self):
        """Test that token cannot be tampered with."""
        data = {"sub": 1, "role": "user"}
        token = create_access_token(data)
        
        # Try to modify token
        parts = token.split('.')
        # Change payload (middle part)
        tampered_token = parts[0] + '.modified.' + parts[2]
        
        # Should fail to decode
        with pytest.raises(JWTError):
            jwt.decode(tampered_token, SECRET_KEY, algorithms=[ALGORITHM])


class TestAuthIntegration:
    """Integration tests for full auth flow."""
    
    def test_password_hash_and_token_flow(self):
        """Test complete flow: hash password, create token."""
        # 1. Hash password
        password = "userPassword123"
        hashed_password = get_password_hash(password)
        
        # 2. Verify password (login)
        assert verify_password(password, hashed_password) is True
        
        # 3. Create token
        user_data = {
            "sub": 1,
            "email": "user@example.com",
            "role": "user"
        }
        token = create_access_token(user_data)
        
        # 4. Decode token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert decoded["sub"] == 1
        assert decoded["email"] == "user@example.com"
        assert decoded["role"] == "user"
    
    def test_role_based_tokens(self):
        """Test tokens for different user roles."""
        roles = ["user", "admin", "partner_lawyer"]
        
        for role in roles:
            data = {"sub": 1, "role": role}
            token = create_access_token(data)
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            assert decoded["role"] == role


# Run tests with: pytest backend/tests/test_auth.py -v
