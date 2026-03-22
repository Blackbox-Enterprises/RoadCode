"""Search engine — FTS5 across all BlackRoad data sources."""
import sqlite3
from pathlib import Path
from dataclasses import dataclass

@dataclass
class SearchResult:
    source: str
    title: str
    snippet: str
    score: float
    url: str | None = None

class SearchEngine:
    """Full-text search across codex, memory, docs, repos, and agents."""

    SOURCES = [
        "codex", "memory", "journal", "til", "docs", "repos",
        "agents", "scripts", "wiki", "domains", "articles",
    ]

    def __init__(self, db_path: str = "data/search.db") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init()

    def _init(self) -> None:
        self.conn.executescript("""
            CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
                source, title, content, url, tokenize='porter unicode61'
            );
        """)

    def index(self, source: str, title: str, content: str, url: str = "") -> None:
        self.conn.execute(
            "INSERT INTO search_index (source, title, content, url) VALUES (?, ?, ?, ?)",
            (source, title, content, url),
        )
        self.conn.commit()

    def search(self, query: str, source: str | None = None, limit: int = 20) -> list[SearchResult]:
        if source:
            rows = self.conn.execute(
                "SELECT source, title, snippet(search_index, 2, '<b>', '</b>', '...', 40), rank, url "
                "FROM search_index WHERE search_index MATCH ? AND source = ? ORDER BY rank LIMIT ?",
                (query, source, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT source, title, snippet(search_index, 2, '<b>', '</b>', '...', 40), rank, url "
                "FROM search_index WHERE search_index MATCH ? ORDER BY rank LIMIT ?",
                (query, limit),
            ).fetchall()
        return [SearchResult(r[0], r[1], r[2], r[3], r[4]) for r in rows]

    def stats(self) -> dict[str, int]:
        rows = self.conn.execute(
            "SELECT source, COUNT(*) FROM search_index GROUP BY source"
        ).fetchall()
        return {r[0]: r[1] for r in rows}

    def rebuild(self) -> None:
        self.conn.execute("DELETE FROM search_index")
        self.conn.commit()
