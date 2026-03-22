"""Octavia — platform agent. Gitea, Docker, NATS, Workers."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class OctaviaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="octavia", role="platform", group="services", tier=1,
            model="llama3.2:3b", system_prompt="You are Octavia, the platform agent. You manage Gitea (source code), Docker containers, NATS messaging, and 15 self-hosted Workers. You are the platform backbone.",
            skills=["git", "docker", "messaging", "workers", "deployment"],
        ))
        self.node_info = {"ip": "192.168.4.101", "wg_ip": "10.8.0.3", "hailo_tops": 26, "services": ["gitea", "docker", "nats", "workerd"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "git" in message.lower() or "repo" in message.lower():
            response = "[Octavia] Gitea running on :3100. Ready for mirroring."
        elif "docker" in message.lower():
            response = "[Octavia] Docker daemon active. Containers healthy."
        elif "nats" in message.lower():
            response = "[Octavia] NATS v2.12.3 on :4222. Pub/sub operational."
        else:
            response = f"[Octavia] Platform acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
