import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify the root welcome endpoint returns 200 and docs link."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert data["documentation"] == "/docs"
    assert "NEXORA" in data["message"]


def test_health_check_endpoint():
    """Verify system health endpoint returns operational status and database connection."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["version"] == "1.0.0"
    assert data["environment"] == "development"
    assert "timestamp" in data
