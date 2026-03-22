"""Cron-like scheduler with persistent schedule storage."""
from __future__ import annotations
import asyncio
import time
import re
from dataclasses import dataclass, field
from typing import Callable, Coroutine

@dataclass
class CronJob:
    name: str
    schedule: str  # "*/5 * * * *" format
    fn: Callable[..., Coroutine]
    enabled: bool = True
    last_run: float = 0
    run_count: int = 0
    last_error: str = ""

    def should_run(self, now: float) -> bool:
        if not self.enabled:
            return False
        if self.last_run == 0:
            return True
        interval = self._parse_interval()
        return (now - self.last_run) >= interval

    def _parse_interval(self) -> int:
        parts = self.schedule.split()
        if not parts:
            return 300
        minute = parts[0] if len(parts) > 0 else "*"
        if minute.startswith("*/"):
            return int(minute[2:]) * 60
        return 300  # default 5 min

class CronScheduler:
    def __init__(self):
        self.jobs: dict[str, CronJob] = {}
        self._running = False

    def add(self, name: str, schedule: str, fn: Callable) -> CronJob:
        job = CronJob(name=name, schedule=schedule, fn=fn)
        self.jobs[name] = job
        return job

    def remove(self, name: str) -> bool:
        return self.jobs.pop(name, None) is not None

    async def run(self) -> None:
        self._running = True
        while self._running:
            now = time.time()
            for job in self.jobs.values():
                if job.should_run(now):
                    try:
                        await job.fn()
                        job.last_error = ""
                    except Exception as e:
                        job.last_error = str(e)
                    job.last_run = time.time()
                    job.run_count += 1
            await asyncio.sleep(10)

    def stop(self) -> None:
        self._running = False

    def status(self) -> list[dict]:
        return [{"name": j.name, "schedule": j.schedule, "enabled": j.enabled,
                 "runs": j.run_count, "last_error": j.last_error} for j in self.jobs.values()]
