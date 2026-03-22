"""Redis-backed key-value store with TTL."""
from __future__ import annotations
import json
import time
from typing import Any

class KVStore:
    """In-memory KV store with TTL (Redis interface when available)."""

    def __init__(self, redis_url: str = "redis://192.168.4.49:6379"):
        self.redis_url = redis_url
        self._store: dict[str, tuple[Any, float]] = {}  # value, expires_at

    def set(self, key: str, value: Any, ttl: int = 0) -> None:
        expires = time.time() + ttl if ttl > 0 else float("inf")
        self._store[key] = (value, expires)

    def get(self, key: str, default: Any = None) -> Any:
        entry = self._store.get(key)
        if entry is None:
            return default
        value, expires = entry
        if time.time() > expires:
            del self._store[key]
            return default
        return value

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def keys(self, pattern: str = "*") -> list[str]:
        now = time.time()
        if pattern == "*":
            return [k for k, (_, exp) in self._store.items() if now < exp]
        prefix = pattern.rstrip("*")
        return [k for k, (_, exp) in self._store.items() if k.startswith(prefix) and now < exp]

    def ttl(self, key: str) -> int:
        entry = self._store.get(key)
        if not entry:
            return -2
        _, expires = entry
        if expires == float("inf"):
            return -1
        remaining = expires - time.time()
        return max(0, int(remaining))

    def flush(self) -> int:
        count = len(self._store)
        self._store.clear()
        return count

    def stats(self) -> dict:
        now = time.time()
        active = sum(1 for _, (_, exp) in self._store.items() if now < exp)
        return {"total_keys": len(self._store), "active_keys": active, "expired": len(self._store) - active}
