"""Service registry — tracks all running services, agents, and nodes."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ServiceEntry:
    name: str
    host: str
    port: int
    status: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)
    registered_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)

    @property
    def is_healthy(self) -> bool:
        return self.status == "healthy" and (time.time() - self.last_heartbeat) < 30

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

class ServiceRegistry:
    """In-memory service registry with health tracking."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceEntry] = {}
        self._listeners: list[callable] = []

    def register(self, name: str, host: str, port: int, **metadata) -> ServiceEntry:
        entry = ServiceEntry(name=name, host=host, port=port, metadata=metadata)
        self._services[name] = entry
        self._notify("registered", entry)
        return entry

    def deregister(self, name: str) -> bool:
        entry = self._services.pop(name, None)
        if entry:
            self._notify("deregistered", entry)
            return True
        return False

    def heartbeat(self, name: str) -> bool:
        if name in self._services:
            self._services[name].last_heartbeat = time.time()
            self._services[name].status = "healthy"
            return True
        return False

    def get(self, name: str) -> ServiceEntry | None:
        return self._services.get(name)

    def list_healthy(self) -> list[ServiceEntry]:
        return [s for s in self._services.values() if s.is_healthy]

    def list_all(self) -> list[ServiceEntry]:
        return list(self._services.values())

    def on_change(self, callback: callable) -> None:
        self._listeners.append(callback)

    def _notify(self, event: str, entry: ServiceEntry) -> None:
        for listener in self._listeners:
            try:
                listener(event, entry)
            except Exception:
                pass
