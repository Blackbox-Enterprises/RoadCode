"""Append-only event store with replay capability."""
from __future__ import annotations
import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class StoredEvent:
    id: int
    stream: str
    event_type: str
    data: dict[str, Any]
    timestamp: float
    version: int

class EventStore:
    def __init__(self, db_path: str = "data/events.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stream TEXT NOT NULL,
                event_type TEXT NOT NULL,
                data TEXT NOT NULL,
                timestamp REAL NOT NULL,
                version INTEGER NOT NULL DEFAULT 1
            );
            CREATE INDEX IF NOT EXISTS idx_stream ON events(stream);
            CREATE INDEX IF NOT EXISTS idx_type ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_ts ON events(timestamp);
        """)

    def append(self, stream: str, event_type: str, data: dict) -> StoredEvent:
        version = self._next_version(stream)
        now = time.time()
        cur = self.conn.execute(
            "INSERT INTO events (stream, event_type, data, timestamp, version) VALUES (?,?,?,?,?)",
            (stream, event_type, json.dumps(data), now, version),
        )
        self.conn.commit()
        return StoredEvent(cur.lastrowid, stream, event_type, data, now, version)

    def _next_version(self, stream: str) -> int:
        row = self.conn.execute("SELECT MAX(version) FROM events WHERE stream = ?", (stream,)).fetchone()
        return (row[0] or 0) + 1

    def replay(self, stream: str, from_version: int = 0) -> list[StoredEvent]:
        rows = self.conn.execute(
            "SELECT id, stream, event_type, data, timestamp, version FROM events WHERE stream = ? AND version > ? ORDER BY version",
            (stream, from_version),
        ).fetchall()
        return [StoredEvent(r[0], r[1], r[2], json.loads(r[3]), r[4], r[5]) for r in rows]

    def query(self, event_type: str | None = None, since: float = 0, limit: int = 100) -> list[StoredEvent]:
        if event_type:
            rows = self.conn.execute(
                "SELECT id, stream, event_type, data, timestamp, version FROM events WHERE event_type = ? AND timestamp > ? ORDER BY timestamp DESC LIMIT ?",
                (event_type, since, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, stream, event_type, data, timestamp, version FROM events WHERE timestamp > ? ORDER BY timestamp DESC LIMIT ?",
                (since, limit),
            ).fetchall()
        return [StoredEvent(r[0], r[1], r[2], json.loads(r[3]), r[4], r[5]) for r in rows]

    def streams(self) -> list[str]:
        return [r[0] for r in self.conn.execute("SELECT DISTINCT stream FROM events").fetchall()]

    def count(self, stream: str | None = None) -> int:
        if stream:
            return self.conn.execute("SELECT COUNT(*) FROM events WHERE stream = ?", (stream,)).fetchone()[0]
        return self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
