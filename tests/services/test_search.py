"""Tests for search engine."""
import pytest
import tempfile
import os
from services.search.engine import SearchEngine

@pytest.fixture
def search_engine():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        engine = SearchEngine(f.name)
        yield engine
    os.unlink(f.name)

def test_index_and_search(search_engine):
    search_engine.index("docs", "WireGuard Setup", "How to configure WireGuard mesh network")
    search_engine.index("docs", "Ollama Models", "Managing AI models with Ollama")
    results = search_engine.search("WireGuard")
    assert len(results) >= 1
    assert results[0].source == "docs"

def test_search_by_source(search_engine):
    search_engine.index("codex", "Fix 1", "Reboot the service")
    search_engine.index("memory", "Note 1", "Remember to check logs")
    results = search_engine.search("service", source="codex")
    assert all(r.source == "codex" for r in results)

def test_stats(search_engine):
    search_engine.index("a", "t1", "c1")
    search_engine.index("b", "t2", "c2")
    stats = search_engine.stats()
    assert isinstance(stats, dict)
