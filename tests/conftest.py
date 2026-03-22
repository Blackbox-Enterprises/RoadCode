"""Test configuration and shared fixtures."""
import pytest
import tempfile
import os

@pytest.fixture
def tmp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def memory_store(tmp_db):
    from core.memory.store import MemoryStore
    return MemoryStore(tmp_db)

@pytest.fixture
def state_manager(tmp_db):
    from core.state import StateManager
    return StateManager(tmp_db)

@pytest.fixture
def registry():
    from core.registry import ServiceRegistry
    return ServiceRegistry()
