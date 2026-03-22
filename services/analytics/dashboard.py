"""Dashboard data aggregation for Prism Console."""
from __future__ import annotations
import time
from dataclasses import dataclass

@dataclass
class DashboardPanel:
    id: str
    title: str
    type: str  # gauge, chart, table, counter
    query: str
    refresh_seconds: int = 30

@dataclass
class DashboardConfig:
    name: str
    panels: list[DashboardPanel]
    refresh_interval: int = 30

FLEET_DASHBOARD = DashboardConfig(
    name="Fleet Overview",
    panels=[
        DashboardPanel("cpu", "CPU Usage", "gauge", "node.*.cpu"),
        DashboardPanel("memory", "Memory Usage", "gauge", "node.*.memory"),
        DashboardPanel("disk", "Disk Usage", "gauge", "node.*.disk"),
        DashboardPanel("requests", "API Requests/min", "counter", "api.requests"),
        DashboardPanel("latency", "P99 Latency", "chart", "api.latency.p99"),
        DashboardPanel("agents", "Active Agents", "counter", "agents.active"),
        DashboardPanel("inference", "Inference Queue", "gauge", "inference.queue.depth"),
        DashboardPanel("errors", "Error Rate", "chart", "api.errors"),
    ],
)

class DashboardAggregator:
    def __init__(self, collector=None):
        self.collector = collector
        self.config = FLEET_DASHBOARD

    def get_panel_data(self, panel_id: str) -> dict:
        panel = next((p for p in self.config.panels if p.id == panel_id), None)
        if not panel:
            return {"error": "panel not found"}
        if self.collector:
            return self.collector.buffer.aggregate(panel.query, minutes=5)
        return {"panel": panel.id, "type": panel.type, "data": [], "ts": time.time()}

    def get_all_panels(self) -> dict:
        return {p.id: self.get_panel_data(p.id) for p in self.config.panels}
