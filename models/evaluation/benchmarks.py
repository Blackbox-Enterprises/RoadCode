"""Model benchmark suite — latency, throughput, quality."""
from __future__ import annotations
import asyncio
import time
import statistics
from dataclasses import dataclass
import httpx

@dataclass
class BenchmarkResult:
    model: str
    node: str
    prompts_tested: int
    avg_latency_ms: float
    p50_latency_ms: float
    p99_latency_ms: float
    tokens_per_second: float
    errors: int

BENCH_PROMPTS = [
    "What is sovereign computing?",
    "Explain the Amundson constant.",
    "Write a Python function to compute fibonacci numbers.",
    "What are the benefits of self-hosted infrastructure?",
    "Describe a WireGuard mesh network.",
]

class ModelBenchmark:
    def __init__(self):
        self.results: list[BenchmarkResult] = []

    async def benchmark_node(self, url: str, model: str, node_name: str, iterations: int = 5) -> BenchmarkResult:
        latencies = []
        total_tokens = 0
        errors = 0
        for prompt in BENCH_PROMPTS[:iterations]:
            try:
                start = time.monotonic()
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.post(f"{url}/api/generate",
                        json={"model": model, "prompt": prompt, "stream": False})
                    data = resp.json()
                    latency = (time.monotonic() - start) * 1000
                    latencies.append(latency)
                    total_tokens += data.get("eval_count", 0)
            except Exception:
                errors += 1
        if not latencies:
            return BenchmarkResult(model, node_name, 0, 0, 0, 0, 0, errors)
        latencies.sort()
        total_time = sum(latencies) / 1000
        result = BenchmarkResult(
            model=model, node=node_name, prompts_tested=len(latencies),
            avg_latency_ms=statistics.mean(latencies),
            p50_latency_ms=latencies[len(latencies)//2],
            p99_latency_ms=latencies[-1],
            tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
            errors=errors,
        )
        self.results.append(result)
        return result

    async def benchmark_fleet(self, model: str = "llama3.2:3b") -> list[BenchmarkResult]:
        nodes = [
            ("cecilia", "http://192.168.4.96:11434"),
            ("lucidia", "http://192.168.4.38:11434"),
            ("gematria", "http://67.205.0.0:11434"),
        ]
        tasks = [self.benchmark_node(url, model, name) for name, url in nodes]
        return await asyncio.gather(*tasks)
