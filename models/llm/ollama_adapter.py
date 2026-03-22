"""Ollama adapter — unified interface for local LLM inference."""
from __future__ import annotations
import json
import httpx
import time
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class ChatResponse:
    message: ChatMessage
    model: str
    total_tokens: int
    latency_ms: float

class OllamaAdapter:
    def __init__(self, base_url: str = "http://192.168.4.96:11434"):
        self.base_url = base_url
        self.default_model = "llama3.2:3b"

    async def chat(self, messages: list[ChatMessage], model: str | None = None,
                   temperature: float = 0.7, max_tokens: int = 2048) -> ChatResponse:
        model = model or self.default_model
        start = time.monotonic()
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            data = resp.json()
            latency = (time.monotonic() - start) * 1000
            return ChatResponse(
                message=ChatMessage("assistant", data.get("message", {}).get("content", "")),
                model=model,
                total_tokens=data.get("eval_count", 0) + data.get("prompt_eval_count", 0),
                latency_ms=latency,
            )

    async def stream_chat(self, messages: list[ChatMessage], model: str | None = None) -> AsyncIterator[str]:
        model = model or self.default_model
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content

    async def embed(self, text: str, model: str = "nomic-embed-text") -> list[float]:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{self.base_url}/api/embeddings",
                                      json={"model": model, "prompt": text})
            return resp.json().get("embedding", [])
