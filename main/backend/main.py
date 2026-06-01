"""
TwinSight — FastAPI Backend
AI-Powered Digital Twin for Autonomous 5G Network Management
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import json
import random
import math
from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

# ─── Routers ──────────────────────────────────────────────────
from routers import (
    dashboard, slices, callflow, auth,
    security, twin, ai_control, incidents, reports
)

# ─── WebSocket Connection Manager ─────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for conn in self.active_connections:
            try:
                await conn.send_json(data)
            except Exception:
                dead.append(conn)
        for d in dead:
            self.disconnect(d)

manager = ConnectionManager()

# ─── Telemetry broadcaster ─────────────────────────────────────
async def telemetry_broadcaster():
    """Continuously broadcast live network telemetry."""
    health = 94.2
    latency = 8.3
    call_success = 97.2

    while True:
        health = max(85, min(100, health + random.uniform(-0.4, 0.4)))
        latency = max(5, min(22, latency + random.uniform(-0.3, 0.3)))
        call_success = max(94, min(99.9, call_success + random.uniform(-0.15, 0.15)))

        payload = {
            "type": "telemetry",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "health": round(health, 1),
                "latency": round(latency, 1),
                "call_success_rate": round(call_success, 1),
                "auth_success_rate": round(random.uniform(97.5, 99.2), 1),
                "ai_confidence": round(random.uniform(88, 96), 1),
                "connected_devices": random.randint(167800, 169000),
                "threat_level": random.randint(55, 70),
                "active_slices": 6,
            }
        }
        await manager.broadcast(payload)
        await asyncio.sleep(3)

# ─── Lifespan ─────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(telemetry_broadcaster())
    yield
    task.cancel()

# ─── App ──────────────────────────────────────────────────────
app = FastAPI(
    title="TwinSight API",
    description="AI-Powered Digital Twin for Autonomous 5G Network Management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include Routers ──────────────────────────────────────────
app.include_router(dashboard.router,   prefix="/api/dashboard",  tags=["Dashboard"])
app.include_router(slices.router,      prefix="/api/slices",     tags=["Network Slices"])
app.include_router(callflow.router,    prefix="/api/callflow",   tags=["Call Flow"])
app.include_router(auth.router,        prefix="/api/auth",       tags=["Authentication"])
app.include_router(security.router,    prefix="/api/security",   tags=["Security SOC"])
app.include_router(twin.router,        prefix="/api/twin",       tags=["Digital Twin"])
app.include_router(ai_control.router,  prefix="/api/ai",         tags=["AI Control"])
app.include_router(incidents.router,   prefix="/api/incidents",  tags=["Incidents"])
app.include_router(reports.router,     prefix="/api/reports",    tags=["Reports"])

# ─── WebSocket endpoint ───────────────────────────────────────
@app.websocket("/ws/telemetry")
async def websocket_telemetry(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            # Handle client commands (e.g. simulation triggers)
            try:
                cmd = json.loads(data)
                if cmd.get("type") == "ping":
                    await ws.send_json({"type": "pong"})
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(ws)

# ─── Health check ─────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database":    "connected",
            "redis":       "connected",
            "ai_engine":   "operational",
            "twin_sync":   "synchronized",
            "websocket":   f"{len(manager.active_connections)} connections",
        }
    }

@app.get("/", tags=["System"])
async def root():
    return {"message": "TwinSight API — 5G Network Intelligence Platform", "docs": "/api/docs"}
