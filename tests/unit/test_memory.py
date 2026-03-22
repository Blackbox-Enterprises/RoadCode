"""Tests for MemoryStore."""

def test_store_and_search(memory_store):
    memory_store.store("test", "greeting", "hello world", tags=["test"])
    results = memory_store.search("hello")
    assert len(results) >= 1

def test_chain_integrity(memory_store):
    memory_store.store("a", "k1", "v1")
    memory_store.store("b", "k2", "v2")
    memory_store.store("c", "k3", "v3")
    valid, count = memory_store.verify_chain()
    assert valid
    assert count == 3

def test_get_by_category(memory_store):
    memory_store.store("solutions", "fix1", "reboot")
    memory_store.store("solutions", "fix2", "clear cache")
    memory_store.store("patterns", "p1", "retry with backoff")
    results = memory_store.get_by_category("solutions")
    assert len(results) == 2
