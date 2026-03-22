"""Base agent — all agents inherit from this."""
from __future__ import annotations
import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    name: str
    role: str
    group: str = "general"
    tier: int = 1
    model: str = "llama3.2:3b"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: str = ""
    skills: list[str] = field(default_factory=list)
    values: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentMessage:
    role: str  # user, assistant, system
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

class BaseAgent(ABC):
    """Base class for all BlackRoad agents."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.history: list[AgentMessage] = []
        self.state: dict[str, Any] = {}
        self.started_at = time.time()
        self._running = False

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def uptime(self) -> float:
        return time.time() - self.started_at

    @abstractmethod
    async def process(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Process incoming message and return response."""
        ...

    async def start(self) -> None:
        self._running = True
        logger.info(f"Agent {self.name} started (role={self.config.role}, model={self.config.model})")
        await self.on_start()

    async def stop(self) -> None:
        self._running = False
        await self.on_stop()
        logger.info(f"Agent {self.name} stopped after {self.uptime:.0f}s")

    async def on_start(self) -> None:
        pass

    async def on_stop(self) -> None:
        pass

    def add_to_history(self, role: str, content: str, **metadata) -> None:
        self.history.append(AgentMessage(role=role, content=content, metadata=metadata))
        if len(self.history) > 200:
            self.history = self.history[-100:]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "role": self.config.role,
            "group": self.config.group,
            "tier": self.config.tier,
            "model": self.config.model,
            "uptime": round(self.uptime),
            "messages": len(self.history),
            "running": self._running,
        }
