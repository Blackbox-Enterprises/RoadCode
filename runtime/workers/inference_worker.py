"""Inference worker — pulls jobs from queue and processes via Ollama."""
from __future__ import annotations
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

class InferenceWorker:
    def __init__(self, node: str = "cecilia", ollama_url: str = "http://192.168.4.96:11434"):
        self.node = node
        self.ollama_url = ollama_url
        self._running = False
        self.processed = 0
        self.errors = 0

    async def run(self, queue=None) -> None:
        self._running = True
        logger.info(f"Inference worker started on {self.node}")
        while self._running:
            if queue and queue.depth > 0:
                task = queue.dequeue()
                if task:
                    try:
                        await self._process(task)
                        queue.complete(task.id)
                        self.processed += 1
                    except Exception as e:
                        queue.fail(task.id)
                        self.errors += 1
                        logger.error(f"Inference failed: {e}")
            await asyncio.sleep(0.1)

    async def _process(self, task) -> dict:
        import httpx
        prompt = task.payload.get("prompt", "")
        model = task.payload.get("model", "llama3.2:3b")
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{self.ollama_url}/api/generate",
                                      json={"model": model, "prompt": prompt, "stream": False})
            return resp.json()

    def stop(self) -> None:
        self._running = False

    def stats(self) -> dict:
        return {"node": self.node, "processed": self.processed, "errors": self.errors, "running": self._running}
