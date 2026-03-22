"""Integration tests for API gateway."""
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from services.gateway.main import app
    return TestClient(app)

def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "online"

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_agents(client):
    resp = client.get("/api/agents")
    assert resp.status_code == 200
    assert len(resp.json()["agents"]) > 0

def test_chat(client):
    resp = client.post("/api/chat", json={"agent": "cece", "message": "hello"})
    assert resp.status_code == 200
    assert "cece" in resp.json()["agent"]
