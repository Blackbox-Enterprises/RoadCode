"""Background worker — processes queued tasks."""
import asyncio
import logging
import signal

logger = logging.getLogger(__name__)

class Worker:
    def __init__(self) -> None:
        self._running = False
        self._processed = 0

    async def run(self) -> None:
        self._running = True
        logger.info("Worker started, waiting for tasks...")
        while self._running:
            await asyncio.sleep(1)

    def stop(self) -> None:
        self._running = False
        logger.info(f"Worker stopped after processing {self._processed} tasks")

async def main():
    worker = Worker()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, worker.stop)
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
