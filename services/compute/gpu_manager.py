"""Hailo-8 GPU manager — model loading, inference queue, accelerator stats."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any
from collections import deque

@dataclass
class AcceleratorInfo:
    node: str
    device: str
    tops: float
    temperature: float = 0.0
    utilization: float = 0.0
    models_loaded: list[str] = field(default_factory=list)

ACCELERATORS = [
    AcceleratorInfo("cecilia", "/dev/hailo0", 26.0),
    AcceleratorInfo("octavia", "/dev/hailo0", 26.0),
]

@dataclass
class InferenceRequest:
    id: str
    model: str
    input_data: Any
    priority: int = 1
    submitted_at: float = field(default_factory=time.time)

@dataclass
class InferenceResult:
    request_id: str
    output: Any
    latency_ms: float
    node: str
    model: str

class GPUManager:
    def __init__(self):
        self.accelerators = {a.node: a for a in ACCELERATORS}
        self.queue: deque[InferenceRequest] = deque()
        self.processing: dict[str, InferenceRequest] = {}
        self.results: list[InferenceResult] = []

    def enqueue(self, request: InferenceRequest) -> int:
        self.queue.append(request)
        return len(self.queue)

    def select_accelerator(self, model: str) -> AcceleratorInfo | None:
        available = [a for a in self.accelerators.values() if a.utilization < 90]
        if not available:
            return None
        return min(available, key=lambda a: a.utilization)

    async def process_next(self) -> InferenceResult | None:
        if not self.queue:
            return None
        request = self.queue.popleft()
        accel = self.select_accelerator(request.model)
        if not accel:
            self.queue.appendleft(request)
            return None
        self.processing[request.id] = request
        accel.utilization = min(100, accel.utilization + 25)
        start = time.monotonic()
        await asyncio.sleep(0.01)  # simulate inference
        latency = (time.monotonic() - start) * 1000
        accel.utilization = max(0, accel.utilization - 25)
        del self.processing[request.id]
        result = InferenceResult(request.id, {"generated": True}, latency, accel.node, request.model)
        self.results.append(result)
        return result

    def stats(self) -> dict:
        return {"queued": len(self.queue), "processing": len(self.processing),
                "completed": len(self.results), "total_tops": sum(a.tops for a in self.accelerators.values()),
                "accelerators": {a.node: {"tops": a.tops, "util": a.utilization} for a in self.accelerators.values()}}
