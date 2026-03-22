"""Metrics collection — CPU, memory, disk, network for fleet nodes."""
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class NodeMetrics:
    node: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_1m: float
    load_5m: float
    load_15m: float
    temperature: Optional[float] = None
    uptime_seconds: int = 0
    timestamp: float = 0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    @property
    def is_critical(self) -> bool:
        return self.cpu_percent > 90 or self.memory_percent > 90 or self.disk_percent > 95

    @property
    def health_score(self) -> float:
        cpu_score = max(0, 100 - self.cpu_percent)
        mem_score = max(0, 100 - self.memory_percent)
        disk_score = max(0, 100 - self.disk_percent)
        return round((cpu_score + mem_score + disk_score) / 3, 1)

class MetricsCollector:
    """Collects and stores metrics from fleet nodes."""

    def __init__(self) -> None:
        self._metrics: dict[str, list[NodeMetrics]] = {}
        self._max_history = 1440  # 24h at 1/min

    def record(self, metrics: NodeMetrics) -> None:
        if metrics.node not in self._metrics:
            self._metrics[metrics.node] = []
        self._metrics[metrics.node].append(metrics)
        if len(self._metrics[metrics.node]) > self._max_history:
            self._metrics[metrics.node] = self._metrics[metrics.node][-self._max_history:]

    def latest(self, node: str) -> NodeMetrics | None:
        history = self._metrics.get(node, [])
        return history[-1] if history else None

    def all_latest(self) -> dict[str, NodeMetrics]:
        return {node: history[-1] for node, history in self._metrics.items() if history}

    def average(self, node: str, minutes: int = 60) -> NodeMetrics | None:
        history = self._metrics.get(node, [])
        cutoff = time.time() - (minutes * 60)
        recent = [m for m in history if m.timestamp > cutoff]
        if not recent:
            return None
        return NodeMetrics(
            node=node,
            cpu_percent=sum(m.cpu_percent for m in recent) / len(recent),
            memory_percent=sum(m.memory_percent for m in recent) / len(recent),
            disk_percent=sum(m.disk_percent for m in recent) / len(recent),
            load_1m=sum(m.load_1m for m in recent) / len(recent),
            load_5m=sum(m.load_5m for m in recent) / len(recent),
            load_15m=sum(m.load_15m for m in recent) / len(recent),
        )
