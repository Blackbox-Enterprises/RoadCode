"""Load balancer — round-robin and least-connections for fleet nodes."""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Backend:
    name: str
    url: str
    weight: int = 1
    healthy: bool = True
    active_connections: int = 0
    total_requests: int = 0
    total_errors: int = 0
    last_check: float = field(default_factory=time.time)

class LoadBalancer:
    def __init__(self, strategy: str = "least-connections"):
        self.strategy = strategy
        self.backends: list[Backend] = []
        self._rr_index = 0

    def add_backend(self, name: str, url: str, weight: int = 1) -> None:
        self.backends.append(Backend(name=name, url=url, weight=weight))

    def remove_backend(self, name: str) -> None:
        self.backends = [b for b in self.backends if b.name != name]

    def select(self) -> Backend | None:
        healthy = [b for b in self.backends if b.healthy]
        if not healthy:
            return None
        if self.strategy == "round-robin":
            return self._round_robin(healthy)
        elif self.strategy == "least-connections":
            return self._least_connections(healthy)
        elif self.strategy == "weighted":
            return self._weighted(healthy)
        return healthy[0]

    def _round_robin(self, backends: list[Backend]) -> Backend:
        self._rr_index = (self._rr_index + 1) % len(backends)
        return backends[self._rr_index]

    def _least_connections(self, backends: list[Backend]) -> Backend:
        return min(backends, key=lambda b: b.active_connections)

    def _weighted(self, backends: list[Backend]) -> Backend:
        return min(backends, key=lambda b: b.active_connections / max(b.weight, 1))

    def connect(self, backend: Backend) -> None:
        backend.active_connections += 1
        backend.total_requests += 1

    def disconnect(self, backend: Backend, error: bool = False) -> None:
        backend.active_connections = max(0, backend.active_connections - 1)
        if error:
            backend.total_errors += 1

    def stats(self) -> dict:
        return {"strategy": self.strategy, "backends": [
            {"name": b.name, "url": b.url, "healthy": b.healthy, "active": b.active_connections,
             "total": b.total_requests, "errors": b.total_errors} for b in self.backends
        ]}
