"""Model manager — pull, push, list models across fleet Ollama instances."""
from __future__ import annotations
import asyncio
import httpx
import time
from dataclasses import dataclass

@dataclass
class ModelInfo:
    name: str
    size_gb: float
    modified_at: str
    digest: str
    node: str

class ModelManager:
    FLEET_URLS = {
        "cecilia": "http://192.168.4.96:11434",
        "lucidia": "http://192.168.4.38:11434",
        "gematria": "http://67.205.0.0:11434",
    }

    def __init__(self):
        self._cache: dict[str, list[ModelInfo]] = {}

    async def list_all(self) -> dict[str, list[ModelInfo]]:
        result = {}
        for node, url in self.FLEET_URLS.items():
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(f"{url}/api/tags")
                    models = []
                    for m in resp.json().get("models", []):
                        models.append(ModelInfo(
                            name=m["name"], size_gb=round(m.get("size", 0) / 1e9, 2),
                            modified_at=m.get("modified_at", ""), digest=m.get("digest", "")[:12], node=node,
                        ))
                    result[node] = models
            except Exception:
                result[node] = []
        self._cache = result
        return result

    async def pull(self, model: str, node: str) -> bool:
        url = self.FLEET_URLS.get(node)
        if not url:
            return False
        try:
            async with httpx.AsyncClient(timeout=600) as client:
                resp = await client.post(f"{url}/api/pull", json={"name": model, "stream": False})
                return resp.status_code == 200
        except Exception:
            return False

    async def delete(self, model: str, node: str) -> bool:
        url = self.FLEET_URLS.get(node)
        if not url:
            return False
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.delete(f"{url}/api/delete", json={"name": model})
                return resp.status_code == 200
        except Exception:
            return False

    async def sync_model(self, model: str, target_nodes: list[str] | None = None) -> dict[str, bool]:
        targets = target_nodes or list(self.FLEET_URLS.keys())
        results = {}
        for node in targets:
            results[node] = await self.pull(model, node)
        return results
