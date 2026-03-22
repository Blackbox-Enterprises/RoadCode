"""Docker container lifecycle management."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum

class ContainerState(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    DEAD = "dead"

@dataclass
class Container:
    id: str
    name: str
    image: str
    state: ContainerState = ContainerState.CREATED
    ports: dict[int, int] = field(default_factory=dict)
    env: dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    node: str = "localhost"

class ContainerManager:
    def __init__(self):
        self.containers: dict[str, Container] = {}

    async def create(self, name: str, image: str, ports: dict[int, int] | None = None,
                     env: dict[str, str] | None = None, node: str = "localhost") -> Container:
        cid = f"{name}-{int(time.time())}"
        container = Container(id=cid, name=name, image=image, ports=ports or {}, env=env or {}, node=node)
        self.containers[cid] = container
        return container

    async def start(self, container_id: str) -> bool:
        c = self.containers.get(container_id)
        if c and c.state in (ContainerState.CREATED, ContainerState.STOPPED):
            c.state = ContainerState.RUNNING
            return True
        return False

    async def stop(self, container_id: str, timeout: int = 10) -> bool:
        c = self.containers.get(container_id)
        if c and c.state == ContainerState.RUNNING:
            c.state = ContainerState.STOPPED
            return True
        return False

    async def remove(self, container_id: str, force: bool = False) -> bool:
        c = self.containers.get(container_id)
        if not c:
            return False
        if c.state == ContainerState.RUNNING and not force:
            return False
        del self.containers[container_id]
        return True

    def list_running(self, node: str | None = None) -> list[Container]:
        containers = [c for c in self.containers.values() if c.state == ContainerState.RUNNING]
        if node:
            containers = [c for c in containers if c.node == node]
        return containers

    def stats(self) -> dict:
        by_state = {}
        for c in self.containers.values():
            by_state[c.state.value] = by_state.get(c.state.value, 0) + 1
        return {"total": len(self.containers), "by_state": by_state}
