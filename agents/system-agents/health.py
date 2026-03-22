"""Health check agent — monitors all services and nodes."""
import asyncio
import httpx
import time
from dataclasses import dataclass

@dataclass
class HealthResult:
    service: str
    url: str
    status: int
    latency_ms: float
    healthy: bool
    error: str | None = None

async def check_health(name: str, url: str, timeout: float = 5.0) -> HealthResult:
    start = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            latency = (time.monotonic() - start) * 1000
            return HealthResult(name, url, resp.status_code, latency, resp.status_code < 400)
    except Exception as e:
        latency = (time.monotonic() - start) * 1000
        return HealthResult(name, url, 0, latency, False, str(e))

async def fleet_health_check(endpoints: dict[str, str]) -> list[HealthResult]:
    tasks = [check_health(name, url) for name, url in endpoints.items()]
    return await asyncio.gather(*tasks)
