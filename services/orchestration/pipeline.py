"""DAG-based task pipeline — define steps with dependencies, execute in order."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PipelineStep:
    name: str
    fn: Callable[..., Coroutine]
    depends_on: list[str] = field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str = ""
    started_at: float = 0
    completed_at: float = 0
    retries: int = 0
    max_retries: int = 2

    @property
    def duration_ms(self) -> float:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at) * 1000
        return 0

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: dict[str, PipelineStep] = {}
        self.context: dict[str, Any] = {}

    def add_step(self, name: str, fn: Callable, depends_on: list[str] | None = None, **kwargs) -> Pipeline:
        self.steps[name] = PipelineStep(name=name, fn=fn, depends_on=depends_on or [], **kwargs)
        return self

    def _ready_steps(self) -> list[PipelineStep]:
        ready = []
        for step in self.steps.values():
            if step.status != StepStatus.PENDING:
                continue
            deps_met = all(
                self.steps[d].status == StepStatus.COMPLETED for d in step.depends_on if d in self.steps
            )
            if deps_met:
                ready.append(step)
        return ready

    async def _run_step(self, step: PipelineStep) -> None:
        step.status = StepStatus.RUNNING
        step.started_at = time.time()
        try:
            step.result = await step.fn(self.context)
            step.status = StepStatus.COMPLETED
        except Exception as e:
            step.error = str(e)
            if step.retries < step.max_retries:
                step.retries += 1
                step.status = StepStatus.PENDING
            else:
                step.status = StepStatus.FAILED
        step.completed_at = time.time()

    async def run(self, context: dict | None = None) -> dict:
        self.context = context or {}
        while True:
            ready = self._ready_steps()
            if not ready:
                break
            await asyncio.gather(*(self._run_step(s) for s in ready))
        failed = [s.name for s in self.steps.values() if s.status == StepStatus.FAILED]
        for step in self.steps.values():
            if step.status == StepStatus.PENDING:
                step.status = StepStatus.SKIPPED
        return {
            "pipeline": self.name,
            "status": "failed" if failed else "completed",
            "steps": {s.name: {"status": s.status.value, "duration_ms": s.duration_ms, "error": s.error} for s in self.steps.values()},
        }
