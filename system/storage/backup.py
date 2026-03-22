"""Automated backup with rotation and verification."""
from __future__ import annotations
import hashlib
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BackupRecord:
    name: str
    source: str
    destination: str
    size_bytes: int
    checksum: str
    created_at: float
    node: str

class BackupManager:
    def __init__(self, backup_root: str = "/opt/backups"):
        self.backup_root = Path(backup_root)
        self.history: list[BackupRecord] = []
        self.retention_days = 30
        self.max_backups = 10

    def backup(self, source: str, name: str, node: str = "localhost") -> BackupRecord:
        src = Path(source)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        dest = self.backup_root / name / timestamp
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copy2(str(src), str(dest))
            size = src.stat().st_size
            checksum = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
        elif src.is_dir():
            archive = shutil.make_archive(str(dest), "gztar", str(src))
            size = Path(archive).stat().st_size
            checksum = hashlib.sha256(Path(archive).read_bytes()).hexdigest()[:16]
        else:
            raise FileNotFoundError(f"Source not found: {source}")
        record = BackupRecord(name, source, str(dest), size, checksum, time.time(), node)
        self.history.append(record)
        return record

    def rotate(self, name: str) -> int:
        backups = [r for r in self.history if r.name == name]
        backups.sort(key=lambda r: r.created_at, reverse=True)
        removed = 0
        for old in backups[self.max_backups:]:
            try:
                Path(old.destination).unlink(missing_ok=True)
                self.history.remove(old)
                removed += 1
            except Exception:
                pass
        return removed

    def verify(self, record: BackupRecord) -> bool:
        dest = Path(record.destination)
        if not dest.exists():
            return False
        actual = hashlib.sha256(dest.read_bytes()).hexdigest()[:16]
        return actual == record.checksum

    def list_backups(self, name: str | None = None) -> list[BackupRecord]:
        if name:
            return [r for r in self.history if r.name == name]
        return list(self.history)
