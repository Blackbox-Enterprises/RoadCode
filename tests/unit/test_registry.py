"""Tests for ServiceRegistry."""
from core.registry import ServiceRegistry

def test_register(registry):
    entry = registry.register("test-svc", "localhost", 8080)
    assert entry.name == "test-svc"
    assert entry.url == "http://localhost:8080"

def test_heartbeat(registry):
    registry.register("svc", "localhost", 8080)
    assert registry.heartbeat("svc")
    assert not registry.heartbeat("nonexistent")

def test_list_healthy(registry):
    registry.register("svc1", "localhost", 8080)
    registry.heartbeat("svc1")
    healthy = registry.list_healthy()
    assert len(healthy) == 1

def test_deregister(registry):
    registry.register("svc", "localhost", 8080)
    assert registry.deregister("svc")
    assert registry.get("svc") is None
