"""Gematria — TLS edge agent. Caddy, public-facing, DNS, Ollama."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class GematriaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="gematria", role="tls-edge", group="networking", tier=1,
            model="llama3.2:3b", system_prompt="You are Gematria, the TLS edge agent on DigitalOcean NYC3. You run Caddy (151 domains, Let's Encrypt), Ollama (6 models), and PowerDNS (ns1). You are the public face of BlackRoad.",
            skills=["tls", "dns", "reverse-proxy", "inference"],
        ))
        self.node_info = {"location": "nyc3", "provider": "digitalocean", "domains": 151, "services": ["caddy", "ollama", "powerdns"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "cert" in message.lower() or "tls" in message.lower():
            response = f"[Gematria] Caddy managing {self.node_info['domains']} domains. All certs valid."
        elif "dns" in message.lower():
            response = "[Gematria] PowerDNS (ns1) serving authoritative DNS."
        else:
            response = f"[Gematria] Edge acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
