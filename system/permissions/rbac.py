"""Role-based access control with agent tiers and resource scoping."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum

class Tier(IntEnum):
    OBSERVER = 0
    AGENT = 1
    OPERATOR = 2
    ADMIN = 3

@dataclass
class Permission:
    resource: str
    actions: list[str]

@dataclass
class Role:
    name: str
    tier: Tier
    permissions: list[Permission] = field(default_factory=list)

ROLES = {
    "viewer": Role("viewer", Tier.OBSERVER, [Permission("*", ["read"])]),
    "agent": Role("agent", Tier.AGENT, [
        Permission("memory", ["read", "write"]),
        Permission("chat", ["read", "write"]),
        Permission("search", ["read"]),
    ]),
    "operator": Role("operator", Tier.OPERATOR, [
        Permission("*", ["read", "write"]),
        Permission("deploy", ["execute"]),
        Permission("fleet", ["manage"]),
    ]),
    "admin": Role("admin", Tier.ADMIN, [Permission("*", ["*"])]),
}

class RBAC:
    def __init__(self):
        self.roles = dict(ROLES)
        self.assignments: dict[str, str] = {}  # agent_name -> role_name

    def assign(self, agent: str, role_name: str) -> bool:
        if role_name not in self.roles:
            return False
        self.assignments[agent] = role_name
        return True

    def check(self, agent: str, resource: str, action: str) -> bool:
        role_name = self.assignments.get(agent)
        if not role_name:
            return False
        role = self.roles[role_name]
        for perm in role.permissions:
            if (perm.resource == "*" or perm.resource == resource):
                if "*" in perm.actions or action in perm.actions:
                    return True
        return False

    def get_tier(self, agent: str) -> Tier:
        role_name = self.assignments.get(agent)
        if not role_name or role_name not in self.roles:
            return Tier.OBSERVER
        return self.roles[role_name].tier

    def list_agents_by_role(self, role_name: str) -> list[str]:
        return [a for a, r in self.assignments.items() if r == role_name]
