"""Process manager — manages system processes with restart policies."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class RestartPolicy(Enum):
    NEVER = "never"
    ON_FAILURE = "on-failure"
    ALWAYS = "always"

class ProcessState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    FAILED = "failed"

@dataclass
class ManagedProcess:
    name: str
    command: str
    restart_policy: RestartPolicy = RestartPolicy.ON_FAILURE
    state: ProcessState = ProcessState.STOPPED
    pid: Optional[int] = None
    started_at: float = 0
    restart_count: int = 0
    max_restarts: int = 5
    last_exit_code: int = 0

    @property
    def uptime(self) -> float:
        return time.time() - self.started_at if self.state == ProcessState.RUNNING else 0

class ProcessManager:
    def __init__(self):
        self.processes: dict[str, ManagedProcess] = {}
        self._tasks: dict[str, asyncio.Task] = {}

    def register(self, name: str, command: str, restart: RestartPolicy = RestartPolicy.ON_FAILURE) -> ManagedProcess:
        proc = ManagedProcess(name=name, command=command, restart_policy=restart)
        self.processes[name] = proc
        return proc

    async def start(self, name: str) -> bool:
        proc = self.processes.get(name)
        if not proc or proc.state == ProcessState.RUNNING:
            return False
        proc.state = ProcessState.STARTING
        self._tasks[name] = asyncio.create_task(self._supervise(proc))
        return True

    async def stop(self, name: str) -> bool:
        proc = self.processes.get(name)
        if not proc:
            return False
        proc.state = ProcessState.STOPPED
        task = self._tasks.pop(name, None)
        if task:
            task.cancel()
        return True

    async def _supervise(self, proc: ManagedProcess) -> None:
        while proc.state != ProcessState.STOPPED:
            proc.state = ProcessState.RUNNING
            proc.started_at = time.time()
            try:
                p = await asyncio.create_subprocess_shell(proc.command)
                proc.pid = p.pid
                proc.last_exit_code = await p.wait()
            except Exception:
                proc.last_exit_code = 1
            if proc.state == ProcessState.STOPPED:
                break
            proc.state = ProcessState.FAILED
            should_restart = (
                proc.restart_policy == RestartPolicy.ALWAYS or
                (proc.restart_policy == RestartPolicy.ON_FAILURE and proc.last_exit_code != 0)
            )
            if should_restart and proc.restart_count < proc.max_restarts:
                proc.restart_count += 1
                await asyncio.sleep(min(30, 2 ** proc.restart_count))
            else:
                break

    def status(self) -> list[dict]:
        return [{"name": p.name, "state": p.state.value, "pid": p.pid,
                 "uptime": round(p.uptime), "restarts": p.restart_count} for p in self.processes.values()]
