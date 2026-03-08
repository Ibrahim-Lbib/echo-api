# Basic unit tests
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_api_key

client = TestClient(app, raise_server_exceptions=False)


# ---- Fixtures ----

async def mock_get_api_key():
    """Bypass real API key validation in tests."""
    return "testkey123"

@pytest.fixture(autouse=False)
def mock_auth():
    """Override FastAPI's API key dependency with a no-op."""
    app.dependency_overrides[get_api_key] = mock_get_api_key
    yield
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def disable_cache():
    """Disable Redis cache for all tests to prevent stale data interference."""
    with patch("app.services.engine.get_cached_recommendations", return_value=None), \
         patch("app.services.engine.set_cached_recommendations", return_value=None):
        yield


# ---- Tests ----

def test_recommendations_basic(mock_auth):
    """Test basic endpoint without user_id"""
    response = client.get("/recommend/?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user_id"] is None
    assert len(data["recommendations"]) == 3

def test_recommendations_with_user(mock_auth):
    """Test with user_id (Supabase will fail in test env, fallback is fine)"""
    response = client.get("/recommend/?user_id=123&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user_id"] == 123
    assert len(data["recommendations"]) == 2

def test_rate_limit(mock_auth):
    """Test that the first request succeeds (rate limit not exceeded)."""
    response = client.get("/recommend/?limit=1")
    assert response.status_code == 200

def test_invalid_limit(mock_auth):
    """Limit > 20 should return 422 Unprocessable Entity"""
    response = client.get("/recommend/?limit=100")
    assert response.status_code == 422

def test_missing_api_key():
    """No API key should return 401 Unauthorized"""
    response = client.get("/recommend/?limit=1")
    assert response.status_code == 401

def test_recommendations_item_shape(mock_auth):
    """Verify response items have the correct fields"""
    response = client.get("/recommend/?limit=1")
    assert response.status_code == 200
    item = response.json()["recommendations"][0]
    assert "id" in item
    assert "name" in item
    assert "category" in item
    assert "score" in item