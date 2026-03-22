"""Latency benchmark tests."""
import pytest
import time
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from services.gateway.main import app
    return TestClient(app)

def test_root_latency(client):
    start = time.monotonic()
    resp = client.get("/")
    latency_ms = (time.monotonic() - start) * 1000
    assert resp.status_code == 200
    assert latency_ms < 100, f"Root endpoint too slow: {latency_ms:.1f}ms"

def test_health_latency(client):
    start = time.monotonic()
    resp = client.get("/health")
    latency_ms = (time.monotonic() - start) * 1000
    assert resp.status_code == 200
    assert latency_ms < 100

def test_agents_latency(client):
    start = time.monotonic()
    resp = client.get("/api/agents")
    latency_ms = (time.monotonic() - start) * 1000
    assert resp.status_code == 200
    assert latency_ms < 200

def test_concurrent_requests(client):
    start = time.monotonic()
    for _ in range(20):
        client.get("/health")
    total_ms = (time.monotonic() - start) * 1000
    avg_ms = total_ms / 20
    assert avg_ms < 50, f"Average latency too high: {avg_ms:.1f}ms"
