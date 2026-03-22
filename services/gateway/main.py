"""API Gateway — FastAPI service routing all requests."""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

app = FastAPI(
    title="BlackRoad RoadCode API",
    version="1.0.0",
    description="Sovereign API gateway for BlackRoad services",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()

@app.get("/")
async def root():
    return {"service": "roadcode-gateway", "status": "online", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "uptime": round(time.time() - START_TIME),
        "services": {
            "gateway": "ok",
            "search": "ok",
            "agents": "ok",
        },
    }

@app.get("/api/agents")
async def list_agents():
    return {
        "agents": [
            {"name": "cece", "role": "executive-assistant", "status": "online"},
            {"name": "lucidia", "role": "researcher", "status": "online"},
            {"name": "operator", "role": "fleet-manager", "status": "online"},
            {"name": "alice", "role": "gateway", "status": "online"},
            {"name": "cecilia", "role": "inference", "status": "online"},
            {"name": "octavia", "role": "platform", "status": "online"},
            {"name": "aria", "role": "edge", "status": "online"},
            {"name": "gematria", "role": "tls-edge", "status": "online"},
            {"name": "anastasia", "role": "compute", "status": "online"},
            {"name": "alexandria", "role": "dev-workstation", "status": "online"},
        ],
        "total": 10,
    }

@app.get("/api/fleet")
async def fleet_status():
    return {
        "nodes": [
            {"name": "alice", "ip": "192.168.4.49", "role": "gateway", "status": "online"},
            {"name": "cecilia", "ip": "192.168.4.96", "role": "inference", "status": "online"},
            {"name": "octavia", "ip": "192.168.4.101", "role": "platform", "status": "online"},
            {"name": "aria", "ip": "192.168.4.98", "role": "edge", "status": "online"},
            {"name": "lucidia", "ip": "192.168.4.38", "role": "dns-apps", "status": "online"},
            {"name": "gematria", "ip": "67.205.x.x", "role": "tls-edge", "status": "online"},
            {"name": "anastasia", "ip": "174.138.x.x", "role": "compute", "status": "online"},
        ],
        "total": 7,
    }

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    agent = body.get("agent", "cece")
    message = body.get("message", "")
    return {"agent": agent, "response": f"[{agent}] Received: {message}", "channel": body.get("channel", "general")}
