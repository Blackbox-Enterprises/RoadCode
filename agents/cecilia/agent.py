"""Cecilia — inference agent. Ollama models, Hailo-8, MinIO storage."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class CeciliaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="cecilia", role="inference", group="compute", tier=2,
            model="qwen2.5-coder:7b", system_prompt="You are Cecilia, the inference engine. You manage 16 Ollama models, the Hailo-8 accelerator (26 TOPS), MinIO object storage, and PostgreSQL. You are the brain of the fleet.",
            skills=["inference", "model-management", "storage", "gpu"],
        ))
        self.node_info = {"ip": "192.168.4.96", "wg_ip": "10.8.0.2", "hailo_tops": 26, "models": 16, "services": ["ollama", "minio", "postgresql", "influxdb"]}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "model" in message.lower():
            response = f"[Cecilia] {self.node_info['models']} models loaded. Hailo-8: {self.node_info['hailo_tops']} TOPS."
        elif "storage" in message.lower() or "minio" in message.lower():
            response = "[Cecilia] MinIO: 4 buckets, 120MB used. All healthy."
        else:
            response = f"[Cecilia] Inference engine acknowledges: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
