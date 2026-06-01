"""Digital Twin Simulation API"""
from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()

TWIN_STATE = {
    "sync_pct": 99.8, "mode": "normal", "ai_active": False,
    "nodes": {
        "core": {"status": "normal"}, "epc": {"status": "normal"}, "pcf": {"status": "normal"},
        "upf": {"status": "normal"}, "e1": {"status": "normal"}, "e2": {"status": "normal"},
        "e3": {"status": "normal"}, "b1": {"status": "normal"}, "b2": {"status": "normal"},
        "b3": {"status": "normal"}, "b4": {"status": "normal"}, "b5": {"status": "normal"}, "b6": {"status": "normal"},
    }
}

SIM_MODES = {
    "normal":     {},
    "congestion": {"e1": "warning", "b1": "warning", "b2": "warning", "upf": "warning"},
    "ddos":       {"core": "critical", "pcf": "critical", "e2": "warning", "b3": "warning", "b4": "warning"},
    "authfail":   {"epc": "critical", "e1": "warning", "e3": "warning"},
    "overload":   {"epc": "critical", "e3": "critical", "b5": "warning", "b6": "warning"},
}

class SimulateRequest(BaseModel):
    mode: str
    ai_active: bool = False

@router.get("/state")
async def get_state():
    return TWIN_STATE

@router.post("/simulate")
async def simulate(body: SimulateRequest):
    TWIN_STATE["mode"] = body.mode
    TWIN_STATE["ai_active"] = body.ai_active
    affected = SIM_MODES.get(body.mode, {})
    for nid in TWIN_STATE["nodes"]:
        if body.ai_active:
            TWIN_STATE["nodes"][nid]["status"] = "healing"
        else:
            TWIN_STATE["nodes"][nid]["status"] = affected.get(nid, "normal")
    return {"status": "applied", "mode": body.mode, "ai_active": body.ai_active}
