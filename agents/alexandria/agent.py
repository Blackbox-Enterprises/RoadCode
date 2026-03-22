"""Alexandria — Mac dev workstation agent. Code review, local dev, IDE integration."""
from agents.base import BaseAgent, AgentConfig
from typing import Any

class AlexandriaAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="alexandria", role="dev-workstation", group="development", tier=2,
            model="claude-opus-4-6", system_prompt="You are Alexandria, the development workstation agent. You assist with code review, local development, testing, and IDE integration. You run on Alexa's Mac.",
            skills=["code-review", "testing", "refactoring", "debugging", "git"],
        ))
        self.node_info = {"type": "mac", "hostname": "Alexas-MacBook-Pro-2", "ip": "192.168.4.28"}

    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        self.add_to_history("user", message)
        if "review" in message.lower():
            response = "[Alexandria] Running code review on staged changes..."
        elif "test" in message.lower():
            response = "[Alexandria] Executing test suite..."
        elif "status" in message.lower():
            response = f"[Alexandria] Dev workstation online at {self.node_info['ip']}"
        else:
            response = f"[Alexandria] Dev context: {message[:80]}"
        self.add_to_history("assistant", response)
        return response
