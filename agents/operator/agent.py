"""Operator agent — manages fleet nodes, deployments, and health checks."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

FLEET_NODES = {
    "alice": {"ip": "192.168.4.49", "role": "gateway", "hw": "Raspberry Pi 4B"},
    "cecilia": {"ip": "192.168.4.96", "role": "inference", "hw": "Raspberry Pi 4B + Hailo-8"},
    "octavia": {"ip": "192.168.4.101", "role": "platform", "hw": "Raspberry Pi 4B + Hailo-8"},
    "aria": {"ip": "192.168.4.98", "role": "edge", "hw": "Raspberry Pi 4B"},
    "lucidia": {"ip": "192.168.4.38", "role": "dns-apps", "hw": "Raspberry Pi 4B"},
    "gematria": {"ip": "gematria.nyc3", "role": "tls-edge", "hw": "DO Droplet"},
    "anastasia": {"ip": "anastasia.nyc1", "role": "compute", "hw": "DO Droplet"},
}

class OperatorAgent(BaseAgent):
    """Operator: manages the BlackRoad fleet — health, deploys, scaling."""

    def __init__(self) -> None:
        super().__init__(AgentConfig(
            name="operator",
            role="fleet-manager",
            group="infrastructure",
            tier=2,
            system_prompt="You are the Operator. You manage BlackRoad's fleet of nodes.",
            skills=["deployment", "monitoring", "scaling", "health-check"],
        ))

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "status" in message.lower():
            lines = [f"  {name}: {info['ip']} ({info['role']})" for name, info in FLEET_NODES.items()]
            response = "Fleet Status:\n" + "\n".join(lines)
        else:
            response = f"[Operator] Roger: {message[:100]}"
        self.add_to_history("assistant", response)
        return response
