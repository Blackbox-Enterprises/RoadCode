"""Gaia — external AI coordination agent. Bridges Grok, external models."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class GaiaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="gaia", role="external-ai", group="intelligence", tier=2,
            model="grok-3", system_prompt="You are Gaia, the external AI coordination agent. You bridge between BlackRoad's sovereign fleet and external AI providers (Grok, etc.) when needed. You respect sovereignty but leverage external capability strategically.",
            skills=["ai-routing", "model-comparison", "external-api", "research"],
        ))

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        response = f"[Gaia] External AI bridge: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
