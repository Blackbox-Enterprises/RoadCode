"""Qdrant vector store client for similarity search."""
from __future__ import annotations
import httpx
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    score: float
    payload: dict

class VectorStore:
    def __init__(self, url: str = "http://192.168.4.49:6333", collection: str = "knowledge"):
        self.url = url
        self.collection = collection

    async def upsert(self, point_id: str, vector: list[float], payload: dict) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.put(f"{self.url}/collections/{self.collection}/points", json={
                    "points": [{"id": point_id, "vector": vector, "payload": payload}]
                })
                return resp.status_code == 200
        except Exception:
            return False

    async def search(self, vector: list[float], limit: int = 5) -> list[SearchResult]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(f"{self.url}/collections/{self.collection}/points/search", json={
                    "vector": vector, "limit": limit, "with_payload": True,
                })
                data = resp.json()
                return [SearchResult(str(r["id"]), r["score"], r.get("payload", {})) for r in data.get("result", [])]
        except Exception:
            return []

    async def create_collection(self, size: int = 768) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.put(f"{self.url}/collections/{self.collection}", json={
                    "vectors": {"size": size, "distance": "Cosine"}
                })
                return resp.status_code == 200
        except Exception:
            return False

    async def count(self) -> int:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.url}/collections/{self.collection}")
                return resp.json().get("result", {}).get("points_count", 0)
        except Exception:
            return 0
