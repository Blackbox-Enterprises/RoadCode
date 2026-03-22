"""Compute dispatcher — routes jobs to fleet nodes by load and capability."""
from __future__ import annotations
import asyncio
import time
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

class JobStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ComputeNode:
    name: str
    ip: str
    capabilities: list[str]
    max_concurrent: int = 4
    current_load: int = 0
    last_heartbeat: float = field(default_factory=time.time)

    @property
    def available_slots(self) -> int:
        return max(0, self.max_concurrent - self.current_load)

    @property
    def is_alive(self) -> bool:
        return (time.time() - self.last_heartbeat) < 60

@dataclass
class ComputeJob:
    id: str
    task_type: str
    payload: dict[str, Any]
    status: JobStatus = JobStatus.QUEUED
    assigned_node: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Any = None
    retries: int = 0
    max_retries: int = 3

FLEET = [
    ComputeNode("cecilia", "192.168.4.96", ["inference", "gpu", "hailo"], 4),
    ComputeNode("octavia", "192.168.4.101", ["inference", "gpu", "hailo", "docker"], 4),
    ComputeNode("alice", "192.168.4.49", ["general", "database", "cache"], 6),
    ComputeNode("lucidia", "192.168.4.38", ["inference", "dns", "general"], 3),
    ComputeNode("gematria", "67.205.0.0", ["inference", "tls", "general"], 8),
    ComputeNode("anastasia", "174.138.0.0", ["general", "batch", "docker"], 8),
]

class ComputeDispatcher:
    def __init__(self, nodes: list[ComputeNode] | None = None):
        self.nodes = {n.name: n for n in (nodes or FLEET)}
        self.jobs: dict[str, ComputeJob] = {}
        self.completed: list[ComputeJob] = []

    def select_node(self, task_type: str) -> ComputeNode | None:
        candidates = [n for n in self.nodes.values() if n.is_alive and n.available_slots > 0 and task_type in n.capabilities]
        if not candidates:
            candidates = [n for n in self.nodes.values() if n.is_alive and n.available_slots > 0]
        if not candidates:
            return None
        return min(candidates, key=lambda n: n.current_load)

    async def submit(self, job_id: str, task_type: str, payload: dict) -> ComputeJob:
        job = ComputeJob(id=job_id, task_type=task_type, payload=payload)
        node = self.select_node(task_type)
        if node:
            job.assigned_node = node.name
            job.status = JobStatus.RUNNING
            node.current_load += 1
        self.jobs[job_id] = job
        return job

    async def complete(self, job_id: str, result: Any = None) -> None:
        job = self.jobs.get(job_id)
        if not job:
            return
        job.status = JobStatus.COMPLETED
        job.completed_at = time.time()
        job.result = result
        if job.assigned_node and job.assigned_node in self.nodes:
            self.nodes[job.assigned_node].current_load -= 1
        self.completed.append(job)

    async def fail(self, job_id: str, error: str) -> bool:
        job = self.jobs.get(job_id)
        if not job:
            return False
        if job.assigned_node and job.assigned_node in self.nodes:
            self.nodes[job.assigned_node].current_load -= 1
        if job.retries < job.max_retries:
            job.retries += 1
            job.status = JobStatus.QUEUED
            job.assigned_node = None
            node = self.select_node(job.task_type)
            if node:
                job.assigned_node = node.name
                job.status = JobStatus.RUNNING
                node.current_load += 1
            return True
        job.status = JobStatus.FAILED
        return False

    def stats(self) -> dict:
        statuses = {}
        for job in self.jobs.values():
            statuses[job.status.value] = statuses.get(job.status.value, 0) + 1
        return {"jobs": len(self.jobs), "completed": len(self.completed), "by_status": statuses,
                "nodes": {n.name: {"load": n.current_load, "slots": n.available_slots, "alive": n.is_alive} for n in self.nodes.values()}}
