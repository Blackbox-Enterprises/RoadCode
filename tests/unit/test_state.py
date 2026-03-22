"""Tests for StateManager."""

def test_set_get(state_manager):
    state_manager.set("key1", {"value": 42})
    assert state_manager.get("key1") == {"value": 42}

def test_get_default(state_manager):
    assert state_manager.get("missing", "default") == "default"

def test_delete(state_manager):
    state_manager.set("key1", "val")
    assert state_manager.delete("key1")
    assert state_manager.get("key1") is None

def test_history(state_manager):
    state_manager.set("key1", "v1")
    state_manager.set("key1", "v2")
    history = state_manager.history("key1")
    assert len(history) == 2

def test_keys(state_manager):
    state_manager.set("app.setting1", "a")
    state_manager.set("app.setting2", "b")
    state_manager.set("other", "c")
    assert len(state_manager.keys("app.")) == 2
