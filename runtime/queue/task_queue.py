"""Task queue — priority queue with dead-letter and retry."""
from __future__ import annotations
import heapq
import time
import json
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

class Priority(IntEnum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3

@dataclass(order=True)
class QueuedTask:
    priority: int
    enqueued_at: float
    id: str = field(compare=False)
    task_type: str = field(compare=False)
    payload: dict[str, Any] = field(compare=False, default_factory=dict)
    retries: int = field(compare=False, default=0)
    max_retries: int = field(compare=False, default=3)

class TaskQueue:
    def __init__(self):
        self._queue: list[QueuedTask] = []
        self._processing: dict[str, QueuedTask] = {}
        self._dead_letter: list[QueuedTask] = []
        self._completed: int = 0

    def enqueue(self, task_id: str, task_type: str, payload: dict,
                priority: Priority = Priority.NORMAL) -> None:
        task = QueuedTask(priority=priority, enqueued_at=time.time(),
                          id=task_id, task_type=task_type, payload=payload)
        heapq.heappush(self._queue, task)

    def dequeue(self) -> QueuedTask | None:
        if not self._queue:
            return None
        task = heapq.heappop(self._queue)
        self._processing[task.id] = task
        return task

    def complete(self, task_id: str) -> None:
        task = self._processing.pop(task_id, None)
        if task:
            self._completed += 1

    def fail(self, task_id: str) -> bool:
        task = self._processing.pop(task_id, None)
        if not task:
            return False
        if task.retries < task.max_retries:
            task.retries += 1
            task.priority = max(0, task.priority - 1)  # bump priority
            heapq.heappush(self._queue, task)
            return True
        self._dead_letter.append(task)
        return False

    def peek(self) -> QueuedTask | None:
        return self._queue[0] if self._queue else None

    @property
    def depth(self) -> int:
        return len(self._queue)

    def stats(self) -> dict:
        return {"queued": len(self._queue), "processing": len(self._processing),
                "completed": self._completed, "dead_letter": len(self._dead_letter)}
