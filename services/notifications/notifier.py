"""Multi-channel notifications — RoundTrip, webhook, email."""
from __future__ import annotations
import asyncio
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

import httpx

class Channel(Enum):
    ROUNDTRIP = "roundtrip"
    WEBHOOK = "webhook"
    LOG = "log"

@dataclass
class Notification:
    title: str
    body: str
    channel: Channel
    severity: str = "info"
    metadata: dict[str, Any] | None = None
    sent_at: float = 0

class Notifier:
    def __init__(self, roundtrip_url: str = "https://roundtrip.blackroad.io"):
        self.roundtrip_url = roundtrip_url
        self.webhooks: list[str] = []
        self.sent: list[Notification] = []

    def add_webhook(self, url: str) -> None:
        self.webhooks.append(url)

    async def send(self, notification: Notification) -> bool:
        notification.sent_at = time.time()
        if notification.channel == Channel.ROUNDTRIP:
            return await self._send_roundtrip(notification)
        elif notification.channel == Channel.WEBHOOK:
            return await self._send_webhooks(notification)
        elif notification.channel == Channel.LOG:
            self.sent.append(notification)
            return True
        return False

    async def _send_roundtrip(self, n: Notification) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(f"{self.roundtrip_url}/api/chat", json={
                    "agent": "system", "message": f"[{n.severity.upper()}] {n.title}: {n.body}",
                    "channel": "alerts",
                })
                self.sent.append(n)
                return resp.status_code == 200
        except Exception:
            return False

    async def _send_webhooks(self, n: Notification) -> bool:
        payload = json.dumps({"title": n.title, "body": n.body, "severity": n.severity, "ts": n.sent_at})
        async with httpx.AsyncClient(timeout=10) as client:
            for url in self.webhooks:
                try:
                    await client.post(url, content=payload, headers={"Content-Type": "application/json"})
                except Exception:
                    continue
        self.sent.append(n)
        return True

    async def alert(self, title: str, body: str, severity: str = "warning") -> None:
        n = Notification(title, body, Channel.ROUNDTRIP, severity)
        await self.send(n)
