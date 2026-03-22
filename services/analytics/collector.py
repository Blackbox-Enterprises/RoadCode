"""Telemetry collector — aggregates metrics from fleet into time-series."""
from __future__ import annotations
import time
import statistics
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class MetricPoint:
    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class TimeSeriesBuffer:
    def __init__(self, max_points: int = 10000):
        self.max_points = max_points
        self.series: dict[str, list[MetricPoint]] = defaultdict(list)

    def record(self, point: MetricPoint) -> None:
        key = f"{point.name}:{','.join(f'{k}={v}' for k, v in sorted(point.tags.items()))}"
        self.series[key].append(point)
        if len(self.series[key]) > self.max_points:
            self.series[key] = self.series[key][-self.max_points:]

    def query(self, name: str, minutes: int = 60, tags: dict | None = None) -> list[MetricPoint]:
        cutoff = time.time() - (minutes * 60)
        results = []
        for key, points in self.series.items():
            if not key.startswith(name + ":") and key != name:
                continue
            for p in points:
                if p.timestamp >= cutoff:
                    if tags and not all(p.tags.get(k) == v for k, v in tags.items()):
                        continue
                    results.append(p)
        return sorted(results, key=lambda p: p.timestamp)

    def aggregate(self, name: str, minutes: int = 60) -> dict:
        points = self.query(name, minutes)
        if not points:
            return {"count": 0}
        values = [p.value for p in points]
        return {"count": len(values), "min": min(values), "max": max(values),
                "avg": statistics.mean(values), "median": statistics.median(values),
                "stddev": statistics.stdev(values) if len(values) > 1 else 0}

class TelemetryCollector:
    def __init__(self):
        self.buffer = TimeSeriesBuffer()
        self.counters: dict[str, int] = defaultdict(int)

    def gauge(self, name: str, value: float, **tags) -> None:
        self.buffer.record(MetricPoint(name, value, tags))

    def counter(self, name: str, increment: int = 1, **tags) -> None:
        key = f"{name}:{tags}"
        self.counters[key] += increment
        self.buffer.record(MetricPoint(name, self.counters[key], tags))

    def timing(self, name: str, duration_ms: float, **tags) -> None:
        self.buffer.record(MetricPoint(f"{name}.timing", duration_ms, tags))

    def fleet_snapshot(self) -> dict:
        nodes = ["alice", "cecilia", "octavia", "aria", "lucidia", "gematria", "anastasia"]
        return {node: self.buffer.aggregate(f"node.{node}.cpu", minutes=5) for node in nodes}
