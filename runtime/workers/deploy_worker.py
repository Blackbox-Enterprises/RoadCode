"""Deploy worker — executes deployment jobs from the queue."""
from __future__ import annotations
import asyncio
import logging
import subprocess
import time

logger = logging.getLogger(__name__)

class DeployWorker:
    def __init__(self):
        self._running = False
        self.deployed = 0

    async def run(self, queue=None) -> None:
        self._running = True
        logger.info("Deploy worker started")
        while self._running:
            if queue and queue.depth > 0:
                task = queue.dequeue()
                if task and task.task_type == "deploy":
                    try:
                        await self._deploy(task.payload)
                        queue.complete(task.id)
                        self.deployed += 1
                    except Exception as e:
                        queue.fail(task.id)
                        logger.error(f"Deploy failed: {e}")
            await asyncio.sleep(1)

    async def _deploy(self, payload: dict) -> None:
        node = payload.get("node", "localhost")
        service = payload.get("service", "")
        version = payload.get("version", "latest")
        logger.info(f"Deploying {service}@{version} to {node}")
        await asyncio.sleep(0.5)  # simulate deploy time

    def stop(self) -> None:
        self._running = False
