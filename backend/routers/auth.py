"""Authentication Analytics API"""
from fastapi import APIRouter
import random
router = APIRouter()

@router.get("/stats")
async def get_auth_stats():
    return {"success_rate": round(random.uniform(97.8, 99.2), 1),
            "failure_rate": round(random.uniform(0.8, 2.2), 1),
            "suspicious_logins": random.randint(200, 300),
            "risk_score": random.randint(28, 38)}

@router.get("/regional-risk")
async def get_regional_risk():
    return [
        {"region": "MUM-North", "failures": 142, "risk": 78, "severity": "high"},
        {"region": "MUM-East",  "failures": 89,  "risk": 54, "severity": "medium"},
        {"region": "MUM-West",  "failures": 32,  "risk": 22, "severity": "low"},
        {"region": "MUM-South", "failures": 67,  "risk": 45, "severity": "medium"},
    ]

@router.get("/heatmap")
async def get_heatmap():
    return [[round(random.uniform(0, 100), 1) for _ in range(24)] for _ in range(7)]
