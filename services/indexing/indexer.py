"""Multi-source indexer — builds unified FTS5 search index."""
from __future__ import annotations
import sqlite3
import time
import json
from pathlib import Path
from dataclasses import dataclass

SOURCES = {
    "codex": {"path": "data/codex.db", "table": "solutions", "fields": ["title", "content"]},
    "tils": {"path": "data/tils.db", "table": "learnings", "fields": ["category", "content"]},
    "journal": {"path": "data/journal.db", "table": "entries", "fields": ["action", "details"]},
    "memory": {"path": "data/memory.db", "table": "memories", "fields": ["key", "value"]},
    "docs": {"path": "docs/", "glob": "**/*.md", "type": "file"},
    "scripts": {"path": "scripts/", "glob": "**/*.sh", "type": "file"},
    "agents": {"path": "agents/", "glob": "**/*.py", "type": "file"},
    "configs": {"path": "config/", "glob": "**/*.yaml", "type": "file"},
}

@dataclass
class IndexEntry:
    source: str
    title: str
    content: str
    url: str = ""
    indexed_at: float = 0

class UnifiedIndexer:
    def __init__(self, index_path: str = "data/search_index.db"):
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(index_path)
        self._init()

    def _init(self):
        self.conn.executescript("""
            CREATE VIRTUAL TABLE IF NOT EXISTS unified_index USING fts5(
                source, title, content, url, tokenize='porter unicode61'
            );
            CREATE TABLE IF NOT EXISTS index_meta (
                source TEXT PRIMARY KEY, last_indexed REAL, entry_count INTEGER
            );
        """)

    def index_files(self, source: str, base_path: str, glob_pattern: str) -> int:
        count = 0
        for filepath in Path(base_path).glob(glob_pattern):
            try:
                content = filepath.read_text(errors="ignore")[:5000]
                self.conn.execute(
                    "INSERT INTO unified_index (source, title, content, url) VALUES (?, ?, ?, ?)",
                    (source, filepath.name, content, str(filepath)),
                )
                count += 1
            except Exception:
                continue
        self.conn.execute(
            "INSERT OR REPLACE INTO index_meta (source, last_indexed, entry_count) VALUES (?, ?, ?)",
            (source, time.time(), count),
        )
        self.conn.commit()
        return count

    def index_db(self, source: str, db_path: str, table: str, fields: list[str]) -> int:
        if not Path(db_path).exists():
            return 0
        src = sqlite3.connect(db_path)
        cols = ", ".join(fields)
        rows = src.execute(f"SELECT {cols} FROM {table}").fetchall()
        count = 0
        for row in rows:
            title = str(row[0])[:200]
            content = " ".join(str(f) for f in row)
            self.conn.execute(
                "INSERT INTO unified_index (source, title, content, url) VALUES (?, ?, ?, ?)",
                (source, title, content, f"{db_path}:{table}"),
            )
            count += 1
        self.conn.commit()
        src.close()
        return count

    def rebuild_all(self) -> dict[str, int]:
        self.conn.execute("DELETE FROM unified_index")
        results = {}
        for name, cfg in SOURCES.items():
            if cfg.get("type") == "file":
                results[name] = self.index_files(name, cfg["path"], cfg["glob"])
            else:
                results[name] = self.index_db(name, cfg["path"], cfg["table"], cfg["fields"])
        return results

    def search(self, query: str, source: str | None = None, limit: int = 20) -> list[dict]:
        if source:
            rows = self.conn.execute(
                "SELECT source, title, snippet(unified_index, 2, '>>>', '<<<', '...', 40), rank, url "
                "FROM unified_index WHERE unified_index MATCH ? AND source = ? ORDER BY rank LIMIT ?",
                (query, source, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT source, title, snippet(unified_index, 2, '>>>', '<<<', '...', 40), rank, url "
                "FROM unified_index WHERE unified_index MATCH ? ORDER BY rank LIMIT ?",
                (query, limit),
            ).fetchall()
        return [{"source": r[0], "title": r[1], "snippet": r[2], "score": r[3], "url": r[4]} for r in rows]

    def stats(self) -> dict:
        rows = self.conn.execute("SELECT source, entry_count, last_indexed FROM index_meta").fetchall()
        return {r[0]: {"count": r[1], "last_indexed": r[2]} for r in rows}
