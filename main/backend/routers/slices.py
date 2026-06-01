"""Network Slices API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import random

router = APIRouter()

SLICES_DB = [
    {"id": "sl1", "name": "eMBB-Enterprise",  "type": "eMBB",  "occ": 72, "tp": "12.4 Gbps", "lat": "8ms",   "users": 4821,  "status": "active",  "sla": 99.7},
    {"id": "sl2", "name": "URLLC-Industrial", "type": "URLLC", "occ": 45, "tp": "2.1 Gbps",  "lat": "1.2ms", "users": 312,   "status": "active",  "sla": 99.99},
    {"id": "sl3", "name": "mMTC-IoT",         "type": "mMTC",  "occ": 88, "tp": "820 Mbps",  "lat": "48ms",  "users": 142000,"status": "warning", "sla": 98.2},
    {"id": "sl4", "name": "eMBB-Consumer",    "type": "eMBB",  "occ": 61, "tp": "8.2 Gbps",  "lat": "12ms",  "users": 18400, "status": "active",  "sla": 99.1},
    {"id": "sl5", "name": "V2X-Automotive",   "type": "V2X",   "occ": 33, "tp": "1.5 Gbps",  "lat": "0.8ms", "users": 890,   "status": "active",  "sla": 99.99},
    {"id": "sl6", "name": "NTN-Satellite",    "type": "NTN",   "occ": 19, "tp": "400 Mbps",  "lat": "600ms", "users": 2100,  "status": "active",  "sla": 97.8},
]

class SliceAction(BaseModel):
    action: str  # scale | pause | fail | heal

@router.get("/")
async def list_slices():
    return SLICES_DB

@router.get("/{slice_id}")
async def get_slice(slice_id: str):
    s = next((x for x in SLICES_DB if x["id"] == slice_id), None)
    if not s:
        raise HTTPException(404, "Slice not found")
    return s

@router.post("/{slice_id}/action")
async def slice_action(slice_id: str, body: SliceAction):
    s = next((x for x in SLICES_DB if x["id"] == slice_id), None)
    if not s:
        raise HTTPException(404, "Slice not found")
    if body.action == "scale":
        s["occ"] = min(100, s["occ"] + 8)
        return {"status": "scaled", "new_occupancy": s["occ"]}
    elif body.action == "pause":
        s["status"] = "paused" if s["status"] != "paused" else "active"
        return {"status": s["status"]}
    elif body.action == "fail":
        s["status"] = "critical"; s["occ"] = 97
        return {"status": "simulated_failure"}
    elif body.action == "heal":
        s["status"] = "active"; s["occ"] = max(20, s["occ"] - 30)
        return {"status": "healed"}
    raise HTTPException(400, "Unknown action")

@router.post("/")
async def create_slice(data: dict):
    new_id = f"sl{len(SLICES_DB)+1}"
    new_slice = {"id": new_id, "occ": 0, "status": "active", "sla": 99.0, **data}
    SLICES_DB.append(new_slice)
    return new_slice
