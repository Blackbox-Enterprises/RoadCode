"""Agent identity system — each agent gets a verifiable identity."""
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentIdentity:
    name: str
    role: str
    node: str
    public_key: str = ""
    fingerprint: str = ""
    registered_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.fingerprint:
            payload = f"{self.name}:{self.role}:{self.node}:{self.registered_at}"
            self.fingerprint = hashlib.sha256(payload.encode()).hexdigest()[:16]

class IdentityRegistry:
    """Registry of all agent identities in the fleet."""

    def __init__(self) -> None:
        self._identities: dict[str, AgentIdentity] = {}

    def register(self, name: str, role: str, node: str, **metadata) -> AgentIdentity:
        identity = AgentIdentity(name=name, role=role, node=node, metadata=metadata)
        self._identities[name] = identity
        return identity

    def get(self, name: str) -> AgentIdentity | None:
        return self._identities.get(name)

    def list_by_node(self, node: str) -> list[AgentIdentity]:
        return [i for i in self._identities.values() if i.node == node]

    def verify(self, name: str, fingerprint: str) -> bool:
        identity = self._identities.get(name)
        return identity is not None and identity.fingerprint == fingerprint
