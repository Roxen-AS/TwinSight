"""Call Flow Analytics API"""
from fastapi import APIRouter
import random
router = APIRouter()

@router.get("/stats")
async def get_stats():
    return {"total_24h": 2840000, "successful": 2760000, "dropped": 28400, "failed": 51200,
            "success_rate": round(random.uniform(96.5, 98.2), 1)}

@router.get("/timeseries")
async def get_timeseries():
    return [{"t": f"{str(i).zfill(2)}:00",
             "success": round(random.uniform(95, 98.5), 1),
             "dropped": round(random.uniform(0.8, 2.0), 1)} for i in range(24)]

@router.get("/failure-reasons")
async def get_failure_reasons():
    return [{"reason": "RAN Congestion", "pct": 34},{"reason": "Core Timeout","pct": 22},
            {"reason": "Handover Fail","pct": 18},{"reason": "UE Unreachable","pct": 14},
            {"reason": "IMS Error","pct": 8},{"reason": "Other","pct": 4}]

@router.get("/recent")
async def get_recent_calls(limit: int = 20):
    statuses = ["active","active","active","critical","warning"]
    nodes = ["gNB-01","gNB-02","gNB-03","gNB-04","gNB-07"]
    slices = ["eMBB","URLLC","V2X"]
    return [{"id": f"C-{8800+i}", "from": random.choice(nodes), "to": "IMS-01",
             "slice": random.choice(slices), "status": random.choice(statuses)} for i in range(limit)]
