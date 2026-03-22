"""Memory store — SQLite + FTS5 full-text search with hash chain integrity."""
from __future__ import annotations
import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class MemoryEntry:
    id: int
    category: str
    key: str
    value: Any
    hash: str
    prev_hash: str | None
    created_at: float
    tags: list[str]

class MemoryStore:
    """Hash-chained memory with full-text search."""

    def __init__(self, db_path: str = "data/memory.db") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init()

    def _init(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                hash TEXT NOT NULL,
                prev_hash TEXT,
                created_at REAL NOT NULL,
                tags TEXT DEFAULT '[]'
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                key, value, tags, content=memories, content_rowid=id
            );
            CREATE INDEX IF NOT EXISTS idx_mem_cat ON memories(category);
            CREATE INDEX IF NOT EXISTS idx_mem_key ON memories(key);
        """)

    def _compute_hash(self, category: str, key: str, value: str, prev: str | None) -> str:
        payload = f"{category}:{key}:{value}:{prev or 'genesis'}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def store(self, category: str, key: str, value: Any, tags: list[str] | None = None) -> MemoryEntry:
        tags = tags or []
        last = self.conn.execute("SELECT hash FROM memories ORDER BY id DESC LIMIT 1").fetchone()
        prev_hash = last[0] if last else None
        serialized = json.dumps(value)
        entry_hash = self._compute_hash(category, key, serialized, prev_hash)
        now = time.time()
        cur = self.conn.execute(
            "INSERT INTO memories (category, key, value, hash, prev_hash, created_at, tags) VALUES (?,?,?,?,?,?,?)",
            (category, key, serialized, entry_hash, prev_hash, now, json.dumps(tags)),
        )
        self.conn.execute(
            "INSERT INTO memories_fts (rowid, key, value, tags) VALUES (?,?,?,?)",
            (cur.lastrowid, key, serialized, " ".join(tags)),
        )
        self.conn.commit()
        return MemoryEntry(cur.lastrowid, category, key, value, entry_hash, prev_hash, now, tags)

    def search(self, query: str, limit: int = 20) -> list[MemoryEntry]:
        rows = self.conn.execute(
            "SELECT m.* FROM memories m JOIN memories_fts f ON m.id = f.rowid WHERE memories_fts MATCH ? LIMIT ?",
            (query, limit),
        ).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def get_by_category(self, category: str) -> list[MemoryEntry]:
        rows = self.conn.execute("SELECT * FROM memories WHERE category = ? ORDER BY created_at DESC", (category,)).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def verify_chain(self) -> tuple[bool, int]:
        rows = self.conn.execute("SELECT * FROM memories ORDER BY id").fetchall()
        verified = 0
        for row in rows:
            entry = self._row_to_entry(row)
            expected = self._compute_hash(entry.category, entry.key, json.dumps(entry.value), entry.prev_hash)
            if expected != entry.hash:
                return False, verified
            verified += 1
        return True, verified

    def _row_to_entry(self, row) -> MemoryEntry:
        return MemoryEntry(row[0], row[1], row[2], json.loads(row[3]), row[4], row[5], row[6], json.loads(row[7]))
