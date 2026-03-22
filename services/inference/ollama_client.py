"""Async Ollama client with retry, fallback, and streaming."""
from __future__ import annotations
import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import AsyncIterator, Any

import httpx

@dataclass
class OllamaNode:
    name: str
    url: str
    priority: int = 0
    healthy: bool = True
    last_check: float = 0
    avg_latency_ms: float = 0

OLLAMA_FLEET = [
    OllamaNode("cecilia", "http://192.168.4.96:11434", 0),
    OllamaNode("lucidia", "http://192.168.4.38:11434", 1),
    OllamaNode("gematria", "http://67.205.0.0:11434", 2),
]

@dataclass
class GenerateResponse:
    text: str
    model: str
    node: str
    tokens: int
    latency_ms: float
    done: bool = True

class OllamaClient:
    def __init__(self, nodes: list[OllamaNode] | None = None, timeout: float = 30.0):
        self.nodes = sorted(nodes or OLLAMA_FLEET, key=lambda n: n.priority)
        self.timeout = timeout

    async def _pick_node(self) -> OllamaNode | None:
        for node in self.nodes:
            if node.healthy:
                return node
        # all unhealthy — try first anyway
        return self.nodes[0] if self.nodes else None

    async def health_check(self, node: OllamaNode) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{node.url}/api/tags")
                node.healthy = resp.status_code == 200
                node.last_check = time.time()
                return node.healthy
        except Exception:
            node.healthy = False
            node.last_check = time.time()
            return False

    async def generate(self, prompt: str, model: str = "llama3.2:3b",
                       system: str = "", max_retries: int = 2) -> GenerateResponse:
        for attempt in range(max_retries + 1):
            node = await self._pick_node()
            if not node:
                raise ConnectionError("No Ollama nodes available")
            try:
                start = time.monotonic()
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    payload = {"model": model, "prompt": prompt, "stream": False}
                    if system:
                        payload["system"] = system
                    resp = await client.post(f"{node.url}/api/generate", json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    latency = (time.monotonic() - start) * 1000
                    node.avg_latency_ms = (node.avg_latency_ms + latency) / 2
                    return GenerateResponse(
                        text=data.get("response", ""),
                        model=model, node=node.name,
                        tokens=data.get("eval_count", 0),
                        latency_ms=latency,
                    )
            except Exception:
                node.healthy = False
                if attempt == max_retries:
                    raise

    async def stream(self, prompt: str, model: str = "llama3.2:3b",
                     system: str = "") -> AsyncIterator[str]:
        node = await self._pick_node()
        if not node:
            raise ConnectionError("No Ollama nodes available")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {"model": model, "prompt": prompt, "stream": True}
            if system:
                payload["system"] = system
            async with client.stream("POST", f"{node.url}/api/generate", json=payload) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]

    async def list_models(self, node_name: str | None = None) -> dict[str, list[str]]:
        result = {}
        targets = [n for n in self.nodes if n.name == node_name] if node_name else self.nodes
        for node in targets:
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    resp = await client.get(f"{node.url}/api/tags")
                    models = [m["name"] for m in resp.json().get("models", [])]
                    result[node.name] = models
            except Exception:
                result[node.name] = []
        return result
