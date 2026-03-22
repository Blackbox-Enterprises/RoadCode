"""Event bus — async pub/sub for inter-service communication."""
from __future__ import annotations
import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine
import time

logger = logging.getLogger(__name__)

@dataclass
class Event:
    topic: str
    payload: Any
    source: str = "unknown"
    timestamp: float = field(default_factory=time.time)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"{self.topic}-{self.timestamp}"

Subscriber = Callable[[Event], Coroutine[Any, Any, None]]

class EventBus:
    """Async event bus with topic-based pub/sub and wildcard support."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self._history: list[Event] = []
        self._max_history = 1000

    def subscribe(self, topic: str, handler: Subscriber) -> None:
        self._subscribers[topic].append(handler)
        logger.debug(f"Subscribed to {topic}: {handler.__name__}")

    def unsubscribe(self, topic: str, handler: Subscriber) -> None:
        if topic in self._subscribers:
            self._subscribers[topic] = [h for h in self._subscribers[topic] if h != handler]

    async def publish(self, event: Event) -> int:
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        handlers = list(self._subscribers.get(event.topic, []))
        handlers.extend(self._subscribers.get("*", []))

        delivered = 0
        for handler in handlers:
            try:
                await handler(event)
                delivered += 1
            except Exception as e:
                logger.error(f"Handler {handler.__name__} failed for {event.topic}: {e}")
        return delivered

    def recent(self, topic: str | None = None, limit: int = 20) -> list[Event]:
        events = self._history if not topic else [e for e in self._history if e.topic == topic]
        return events[-limit:]
