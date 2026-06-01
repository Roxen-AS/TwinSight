"""AI Control Center API"""
from fastapi import APIRouter
from pydantic import BaseModel
import random
router = APIRouter()

AI_MODE = {"mode": "auto"}

class ModeUpdate(BaseModel):
    mode: str  # auto | manual

@router.get("/predictions")
async def get_predictions():
    return [
        {"title": "Slice Congestion Prob.", "val": round(random.uniform(68, 78), 1), "threshold": 70, "node": "mMTC-IoT", "trend": +8},
        {"title": "Auth Failure Prob.",      "val": round(random.uniform(30, 38), 1), "threshold": 50, "node": "IMS Cluster", "trend": -3},
        {"title": "DDoS Attack Prob.",       "val": round(random.uniform(64, 72), 1), "threshold": 60, "node": "Core Network","trend": +12},
        {"title": "Call Failure Prob.",      "val": round(random.uniform(10, 15), 1), "threshold": 30, "node": "VoNR Layer", "trend": -1},
    ]

@router.get("/mode")
async def get_mode():
    return AI_MODE

@router.post("/mode")
async def set_mode(body: ModeUpdate):
    AI_MODE["mode"] = body.mode
    return AI_MODE

@router.post("/recommendations/{rec_id}/approve")
async def approve_recommendation(rec_id: int):
    return {"status": "approved", "rec_id": rec_id, "executed": True}

@router.post("/recommendations/{rec_id}/reject")
async def reject_recommendation(rec_id: int):
    return {"status": "rejected", "rec_id": rec_id}
