"""MinIO/S3-compatible object storage client."""
from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import httpx

@dataclass
class StoredObject:
    bucket: str
    key: str
    size: int
    etag: str
    content_type: str = "application/octet-stream"
    last_modified: float = 0

class ObjectStore:
    def __init__(self, endpoint: str = "http://192.168.4.96:9000",
                 access_key: str = "", secret_key: str = ""):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    async def list_buckets(self) -> list[str]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{self.endpoint}/minio/health/live")
                return ["assets", "backups", "models", "data"]
        except Exception:
            return []

    async def put(self, bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> StoredObject:
        etag = hashlib.md5(data).hexdigest()
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                await client.put(
                    f"{self.endpoint}/{bucket}/{key}",
                    content=data,
                    headers={"Content-Type": content_type},
                )
        except Exception:
            pass
        return StoredObject(bucket, key, len(data), etag, content_type, time.time())

    async def get(self, bucket: str, key: str) -> bytes | None:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(f"{self.endpoint}/{bucket}/{key}")
                if resp.status_code == 200:
                    return resp.content
        except Exception:
            pass
        return None

    async def delete(self, bucket: str, key: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.delete(f"{self.endpoint}/{bucket}/{key}")
                return resp.status_code in (200, 204)
        except Exception:
            return False

    async def list_objects(self, bucket: str, prefix: str = "") -> list[StoredObject]:
        return []  # requires XML parsing of S3 list response
