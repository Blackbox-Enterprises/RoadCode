"""Multi-tenant isolation — each customer gets isolated resources."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Tenant:
    id: str
    name: str
    plan: str = "starter"
    storage_limit_gb: int = 10
    agent_limit: int = 5
    custom_domain: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

class TenantManager:
    def __init__(self):
        self._tenants: dict[str, Tenant] = {}

    def create(self, tenant_id: str, name: str, plan: str = "starter") -> Tenant:
        limits = {"starter": (10, 5), "pro": (100, 50), "enterprise": (1000, 500)}
        storage, agents = limits.get(plan, (10, 5))
        tenant = Tenant(tenant_id, name, plan, storage, agents)
        self._tenants[tenant_id] = tenant
        return tenant

    def get(self, tenant_id: str) -> Tenant | None:
        return self._tenants.get(tenant_id)

    def list_all(self) -> list[Tenant]:
        return list(self._tenants.values())
