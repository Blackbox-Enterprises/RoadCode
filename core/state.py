"""Distributed state manager — SQLite-backed with event sourcing."""
from __future__ import annotations
import json
import sqlite3
import time
from pathlib import Path
from typing import Any

class StateManager:
    """Manages application state with event log and snapshots."""

    def __init__(self, db_path: str = "data/state.db") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                action TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                timestamp REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_events_key ON events(key);
            CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
        """)

    def get(self, key: str, default: Any = None) -> Any:
        row = self.conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        if row is None:
            return default
        return json.loads(row[0])

    def set(self, key: str, value: Any) -> None:
        now = time.time()
        old = self.get(key)
        serialized = json.dumps(value)
        self.conn.execute(
            "INSERT OR REPLACE INTO state (key, value, updated_at) VALUES (?, ?, ?)",
            (key, serialized, now),
        )
        self.conn.execute(
            "INSERT INTO events (key, action, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?)",
            (key, "set", json.dumps(old) if old is not None else None, serialized, now),
        )
        self.conn.commit()

    def delete(self, key: str) -> bool:
        old = self.get(key)
        if old is None:
            return False
        self.conn.execute("DELETE FROM state WHERE key = ?", (key,))
        self.conn.execute(
            "INSERT INTO events (key, action, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?)",
            (key, "delete", json.dumps(old), None, time.time()),
        )
        self.conn.commit()
        return True

    def history(self, key: str, limit: int = 50) -> list[dict]:
        rows = self.conn.execute(
            "SELECT action, old_value, new_value, timestamp FROM events WHERE key = ? ORDER BY timestamp DESC LIMIT ?",
            (key, limit),
        ).fetchall()
        return [{"action": r[0], "old": json.loads(r[1]) if r[1] else None,
                 "new": json.loads(r[2]) if r[2] else None, "ts": r[3]} for r in rows]

    def keys(self, prefix: str = "") -> list[str]:
        rows = self.conn.execute(
            "SELECT key FROM state WHERE key LIKE ?", (f"{prefix}%",)
        ).fetchall()
        return [r[0] for r in rows]

    def close(self) -> None:
        self.conn.close()
