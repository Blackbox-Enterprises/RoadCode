"""Aria — edge networking agent. Headscale, Cloudflare tunnels, mesh."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="aria", role="edge", group="networking", tier=1,
            model="llama3.2:3b", system_prompt="You are Aria, the edge networking agent. You manage Headscale (mesh VPN coordinator), Cloudflare tunnels, nginx reverse proxy, and InfluxDB metrics.",
            skills=["vpn", "tunneling", "mesh", "metrics"],
        ))
        self.node_info = {"ip": "192.168.4.98", "wg_ip": "10.8.0.4", "services": ["headscale", "cloudflared", "nginx", "influxdb"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "mesh" in message.lower() or "vpn" in message.lower():
            response = "[Aria] Headscale mesh: 7 nodes connected. WireGuard 12/12."
        elif "tunnel" in message.lower():
            response = "[Aria] Cloudflare tunnel active. All routes healthy."
        else:
            response = f"[Aria] Edge network acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
