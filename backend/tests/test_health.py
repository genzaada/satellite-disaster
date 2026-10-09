"""Automated tests for health check endpoint."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_returns_200():
    """Verify GET /health returns HTTP 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


def test_health_check_invalid_method():
    """Verify POST /health is not allowed."""
    response = client.post("/health")
    assert response.status_code == 405
