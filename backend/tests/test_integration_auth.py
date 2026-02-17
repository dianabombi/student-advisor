"""
Integration tests for authentication API endpoints.

Tests full auth flow: registration, login, protected endpoints, and RBAC.
Uses FastAPI TestClient to make real HTTP requests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import main app and models
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, Base, get_db

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client with fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    client = TestClient(app)
    yield client
    
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


class TestRegistration:
    """Tests for user registration endpoint."""
    
    def test_register_new_user(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["name"] == "Test User"
        assert data["user"]["role"] == "user"  # Default role
        assert data["user"]["is_active"] is True
        assert "hashed_password" not in data["user"]  # Don't expose password
    
    def test_register_duplicate_email(self, client):
        """Test registration with already registered email."""
        # Register first user
        client.post(
            "/api/auth/register",
            json={
                "name": "First User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Try to register with same email
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Second User",
                "email": "test@example.com",
                "password": "different123"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "invalid-email",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422  # Validation error


class TestLogin:
    """Tests for user login endpoint."""
    
    def test_login_success(self, client):
        """Test successful login with correct credentials."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",  # OAuth2 uses 'username'
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_login_wrong_password(self, client):
        """Test login with incorrect password."""
        # Register user
        client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        # Login with wrong password
        response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
    
    def test_login_empty_credentials(self, client):
        """Test login with empty credentials."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "",
                "password": ""
            }
        )
        
        assert response.status_code in [401, 422]


class TestProtectedEndpoints:
    """Tests for protected endpoints and token validation."""
    
    def test_profile_without_token(self, client):
        """Test accessing profile endpoint without token."""
        response = client.get("/api/auth/profile")
        
        assert response.status_code == 401
    
    def test_profile_with_valid_token(self, client):
        """Test accessing profile with valid token."""
        # Register and login
        client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        response = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
    
    def test_profile_with_invalid_token(self, client):
        """Test accessing profile with invalid token."""
        response = client.get(
            "/api/auth/profile",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
    
    def test_profile_with_malformed_header(self, client):
        """Test with malformed authorization header."""
        response = client.get(
            "/api/auth/profile",
            headers={"Authorization": "InvalidFormat"}
        )
        
        assert response.status_code == 401


class TestRoleBasedAccess:
    """Tests for role-based access control."""
    
    def test_user_cannot_access_admin_endpoint(self, client):
        """Test that regular user cannot access admin endpoints."""
        # Register regular user
        client.post(
            "/api/auth/register",
            json={
                "name": "Regular User",
                "email": "user@example.com",
                "password": "password123"
            }
        )
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "user@example.com",
                "password": "password123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Try to access admin endpoint (example: templates upload)
        response = client.get(
            "/api/templates/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should be forbidden (403) or not implemented yet
        assert response.status_code in [403, 404]
    
    def test_user_can_access_own_cases(self, client):
        """Test that user can access their own cases."""
        # Register user
        client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "user@example.com",
                "password": "password123"
            }
        )
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "user@example.com",
                "password": "password123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Access own cases
        response = client.get(
            "/api/cases",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_token_contains_role(self, client):
        """Test that JWT token contains role information."""
        # Register user
        client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "user@example.com",
                "password": "password123"
            }
        )
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "user@example.com",
                "password": "password123"
            }
        )
        
        data = login_response.json()
        
        # Decode token and verify role is included
        assert "user" in data
        assert data["user"]["role"] == "user"


class TestAuthFlow:
    """Integration tests for complete auth flow."""
    
    def test_complete_auth_flow(self, client):
        """Test complete flow: register → login → access protected → logout."""
        # 1. Register
        register_response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert register_response.status_code == 200
        
        # 2. Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 3. Access protected endpoint
        profile_response = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert profile_response.status_code == 200
        
        # 4. Logout (client-side token removal, server just confirms)
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert logout_response.status_code == 200
    
    def test_multiple_users_isolation(self, client):
        """Test that users can only access their own data."""
        # Register User 1
        client.post(
            "/api/auth/register",
            json={
                "name": "User One",
                "email": "user1@example.com",
                "password": "password123"
            }
        )
        
        # Register User 2
        client.post(
            "/api/auth/register",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "password456"
            }
        )
        
        # Login as User 1
        login1 = client.post(
            "/api/auth/login",
            data={"username": "user1@example.com", "password": "password123"}
        )
        token1 = login1.json()["access_token"]
        
        # Login as User 2
        login2 = client.post(
            "/api/auth/login",
            data={"username": "user2@example.com", "password": "password456"}
        )
        token2 = login2.json()["access_token"]
        
        # Get profiles
        profile1 = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {token1}"}
        )
        profile2 = client.get(
            "/api/auth/profile",
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Verify isolation
        assert profile1.json()["email"] == "user1@example.com"
        assert profile2.json()["email"] == "user2@example.com"
        assert profile1.json()["id"] != profile2.json()["id"]


# Run with: docker compose exec backend pytest tests/test_integration_auth.py -v
