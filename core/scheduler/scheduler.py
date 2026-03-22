"""Scheduler — priority-based task execution with retry logic."""
from __future__ import annotations
import asyncio
import heapq
import logging
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

class Priority(IntEnum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4

@dataclass(order=True)
class ScheduledTask:
    priority: int
    run_at: float
    name: str = field(compare=False)
    fn: Callable = field(compare=False, repr=False)
    args: tuple = field(default=(), compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    retries: int = field(default=3, compare=False)
    retry_delay: float = field(default=1.0, compare=False)

class Scheduler:
    """Priority queue scheduler with retry and backoff."""

    def __init__(self) -> None:
        self._queue: list[ScheduledTask] = []
        self._running = False
        self._completed: list[dict] = []

    def schedule(self, name: str, fn: Callable, priority: Priority = Priority.NORMAL,
                 delay: float = 0, retries: int = 3, **kwargs) -> None:
        task = ScheduledTask(
            priority=priority, run_at=time.time() + delay,
            name=name, fn=fn, kwargs=kwargs, retries=retries,
        )
        heapq.heappush(self._queue, task)

    async def run(self) -> None:
        self._running = True
        while self._running and self._queue:
            task = heapq.heappop(self._queue)
            now = time.time()
            if task.run_at > now:
                await asyncio.sleep(task.run_at - now)
            try:
                result = await task.fn(*task.args, **task.kwargs) if asyncio.iscoroutinefunction(task.fn) else task.fn(*task.args, **task.kwargs)
                self._completed.append({"name": task.name, "status": "ok", "result": result, "ts": time.time()})
            except Exception as e:
                logger.error(f"Task {task.name} failed: {e}")
                if task.retries > 0:
                    task.retries -= 1
                    task.run_at = time.time() + task.retry_delay
                    task.retry_delay *= 2
                    heapq.heappush(self._queue, task)
                else:
                    self._completed.append({"name": task.name, "status": "failed", "error": str(e), "ts": time.time()})

    def stop(self) -> None:
        self._running = False

    @property
    def pending(self) -> int:
        return len(self._queue)
