"""WebSocket handler — real-time agent communication."""
from fastapi import WebSocket, WebSocketDisconnect
import json
import time

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, client_id: str) -> None:
        await ws.accept()
        self.active[client_id] = ws

    def disconnect(self, client_id: str) -> None:
        self.active.pop(client_id, None)

    async def send(self, client_id: str, data: dict) -> None:
        ws = self.active.get(client_id)
        if ws:
            await ws.send_json(data)

    async def broadcast(self, data: dict) -> None:
        for ws in self.active.values():
            await ws.send_json(data)

manager = ConnectionManager()

async def ws_endpoint(ws: WebSocket, client_id: str):
    await manager.connect(ws, client_id)
    try:
        while True:
            data = await ws.receive_json()
            response = {"agent": data.get("agent", "system"), "message": data.get("message", ""), "ts": time.time()}
            await manager.send(client_id, response)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
