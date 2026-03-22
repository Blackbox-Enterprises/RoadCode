"""Model router — selects optimal model based on task and available compute."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelEndpoint:
    name: str
    node: str
    port: int
    model_id: str
    max_tokens: int
    capabilities: list[str]

FLEET_MODELS = [
    ModelEndpoint("cecilia-llama", "192.168.4.96", 11434, "llama3.2:3b", 4096, ["chat", "code"]),
    ModelEndpoint("cecilia-qwen", "192.168.4.96", 11434, "qwen2.5-coder:7b", 8192, ["code", "reasoning"]),
    ModelEndpoint("lucidia-custom", "192.168.4.38", 11434, "lucidia:latest", 4096, ["chat", "reasoning", "math"]),
    ModelEndpoint("gematria-llama", "gematria", 11434, "llama3.2:3b", 4096, ["chat", "code"]),
    ModelEndpoint("gematria-mistral", "gematria", 11434, "mistral:7b", 8192, ["chat", "reasoning"]),
]

class ModelRouter:
    """Routes inference requests to the best available model."""

    def __init__(self, models: list[ModelEndpoint] | None = None) -> None:
        self.models = models or FLEET_MODELS

    def select(self, task: str = "chat", prefer_node: str | None = None) -> ModelEndpoint | None:
        candidates = [m for m in self.models if task in m.capabilities]
        if prefer_node:
            node_match = [m for m in candidates if m.node == prefer_node]
            if node_match:
                return node_match[0]
        return candidates[0] if candidates else None

    def list_by_capability(self, capability: str) -> list[ModelEndpoint]:
        return [m for m in self.models if capability in m.capabilities]

    def list_by_node(self, node: str) -> list[ModelEndpoint]:
        return [m for m in self.models if m.node == node]
