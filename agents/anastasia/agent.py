"""Anastasia — secondary compute agent. Batch processing, Docker."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class AnastasiaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="anastasia", role="compute", group="compute", tier=1,
            model="llama3.2:3b", system_prompt="You are Anastasia, the secondary compute node on DigitalOcean NYC1. You handle batch processing, Docker workloads, and overflow compute.",
            skills=["batch-processing", "docker", "compute"],
        ))
        self.node_info = {"location": "nyc1", "provider": "digitalocean", "services": ["docker", "compute-worker"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        response = f"[Anastasia] Compute node acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
