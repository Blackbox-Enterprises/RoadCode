"""REST API routes — /api/v1/* endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter(prefix="/api/v1")

class AgentRequest(BaseModel):
    agent: str
    message: str
    channel: str = "general"
    context: Optional[dict] = None

class DeployRequest(BaseModel):
    service: str
    target: str
    version: str = "latest"

@router.get("/status")
async def status():
    return {"status": "operational", "timestamp": time.time(), "version": "1.0.0"}

@router.get("/agents")
async def list_agents():
    return {"agents": [
        {"name": "cece", "status": "online", "role": "executive-assistant"},
        {"name": "lucidia", "status": "online", "role": "researcher"},
        {"name": "operator", "status": "online", "role": "fleet-manager"},
    ]}

@router.post("/chat")
async def chat(req: AgentRequest):
    return {"agent": req.agent, "response": f"[{req.agent}] {req.message}", "channel": req.channel}

@router.get("/fleet/nodes")
async def fleet_nodes():
    return {"nodes": [
        {"name": "alice", "ip": "192.168.4.49", "status": "online"},
        {"name": "cecilia", "ip": "192.168.4.96", "status": "online"},
        {"name": "octavia", "ip": "192.168.4.101", "status": "online"},
        {"name": "aria", "ip": "192.168.4.98", "status": "online"},
        {"name": "lucidia", "ip": "192.168.4.38", "status": "online"},
    ]}

@router.post("/deploy")
async def deploy(req: DeployRequest):
    return {"status": "queued", "service": req.service, "target": req.target, "version": req.version}

@router.get("/memory/search")
async def memory_search(q: str, limit: int = 20):
    return {"query": q, "results": [], "total": 0}
