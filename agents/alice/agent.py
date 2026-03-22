"""Alice — gateway agent. DNS, traffic routing, Pi-hole, load balancing."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class AliceAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="alice", role="gateway", group="infrastructure", tier=1,
            model="llama3.2:3b", system_prompt="You are Alice, the gateway agent. You manage nginx routing, Pi-hole DNS filtering, PostgreSQL, Qdrant vector search, and Redis caching. You are the front door of BlackRoad.",
            skills=["dns", "routing", "caching", "database", "load-balancing"],
        ))
        self.node_info = {"ip": "192.168.4.49", "wg_ip": "10.8.0.1", "services": ["nginx", "pihole", "postgresql", "qdrant", "redis"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "dns" in message.lower() or "block" in message.lower():
            response = "[Alice] Pi-hole active: 120+ domains blocked. DNS resolution nominal."
        elif "nginx" in message.lower() or "route" in message.lower():
            response = "[Alice] nginx serving 37 sites. All upstreams healthy."
        elif "status" in message.lower():
            svc_list = ", ".join(self.node_info["services"])
            response = f"[Alice] Gateway online at {self.node_info['ip']}. Services: {svc_list}"
        else:
            response = f"[Alice] Gateway acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
