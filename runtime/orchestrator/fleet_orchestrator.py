"""Fleet orchestrator — coordinates deployments across all nodes."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class DeployStatus(Enum):
    PENDING = "pending"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class DeployTarget:
    node: str
    service: str
    version: str
    status: DeployStatus = DeployStatus.PENDING
    started_at: float = 0
    completed_at: float = 0
    error: str = ""

@dataclass
class Deployment:
    id: str
    targets: list[DeployTarget]
    strategy: str = "rolling"  # rolling, canary, blue-green
    created_at: float = field(default_factory=time.time)

FLEET_SERVICES = {
    "alice": ["nginx", "pihole", "postgresql", "qdrant", "redis"],
    "cecilia": ["ollama", "minio", "postgresql"],
    "octavia": ["gitea", "docker", "nats", "workerd"],
    "aria": ["headscale", "cloudflared", "nginx"],
    "lucidia": ["powerdns", "nginx", "ollama"],
    "gematria": ["caddy", "ollama", "powerdns"],
    "anastasia": ["docker", "compute-worker"],
}

class FleetOrchestrator:
    def __init__(self):
        self.deployments: list[Deployment] = []

    async def deploy(self, service: str, version: str, nodes: list[str] | None = None,
                     strategy: str = "rolling") -> Deployment:
        if nodes is None:
            nodes = [n for n, svcs in FLEET_SERVICES.items() if service in svcs]
        targets = [DeployTarget(node=n, service=service, version=version) for n in nodes]
        deployment = Deployment(id=f"deploy-{int(time.time())}", targets=targets, strategy=strategy)
        self.deployments.append(deployment)
        if strategy == "rolling":
            await self._rolling_deploy(deployment)
        return deployment

    async def _rolling_deploy(self, deployment: Deployment) -> None:
        for target in deployment.targets:
            target.status = DeployStatus.DEPLOYING
            target.started_at = time.time()
            try:
                await asyncio.sleep(0.1)  # simulate deploy
                target.status = DeployStatus.DEPLOYED
            except Exception as e:
                target.status = DeployStatus.FAILED
                target.error = str(e)
            target.completed_at = time.time()

    async def rollback(self, deployment_id: str) -> bool:
        dep = next((d for d in self.deployments if d.id == deployment_id), None)
        if not dep:
            return False
        for target in dep.targets:
            target.status = DeployStatus.ROLLED_BACK
        return True

    def status(self) -> list[dict]:
        return [{"id": d.id, "strategy": d.strategy,
                 "targets": [{"node": t.node, "status": t.status.value} for t in d.targets]}
                for d in self.deployments[-10:]]
