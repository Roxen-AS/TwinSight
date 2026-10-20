"""Security Operations Center API"""
from fastapi import APIRouter
import random
router = APIRouter()

THREATS = [
    {"id": "THR-2201","type": "DDoS","sev": "critical","origin": "External AS","target": "Core Network","risk": 94,"status": "active","t": "12m ago"},
    {"id": "THR-2198","type": "Brute Force","sev": "high","origin": "Region-MUM","target": "IMS Cluster","risk": 76,"status": "monitoring","t": "34m ago"},
    {"id": "THR-2195","type": "Port Scan","sev": "medium","origin": "EDGE-02","target": "eMBB Slice","risk": 58,"status": "mitigated","t": "1h ago"},
    {"id": "THR-2190","type": "Config Drift","sev": "low","origin": "gNB-011","target": "RAN Layer","risk": 32,"status": "resolved","t": "4h ago"},
]

@router.get("/threats")
async def list_threats():
    return THREATS

@router.get("/threat-level")
async def get_threat_level():
    return {"score": random.randint(58, 68), "level": "MEDIUM", "ai_confidence": 87}

@router.get("/ai-predictions")
async def get_ai_predictions():
    return [
        {"type": "DDoS Probability",  "val": round(random.uniform(62, 74), 1)},
        {"type": "Brute Force Risk",  "val": round(random.uniform(38, 48), 1)},
        {"type": "Port Scan Active",  "val": round(random.uniform(76, 86), 1)},
        {"type": "Config Drift",      "val": round(random.uniform(25, 35), 1)},
    ]
