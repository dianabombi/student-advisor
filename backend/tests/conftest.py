"""Test configuration and fixtures."""

import pytest


@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "database_url": "postgresql://user:password@localhost:5433/codex_test_db",
        "openai_api_key": "test_key",
        "test_user_email": "test@example.com",
        "test_user_password": "testpassword123"
    }
