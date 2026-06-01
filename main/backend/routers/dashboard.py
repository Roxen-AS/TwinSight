"""Dashboard API — Network KPIs and overview metrics."""
from fastapi import APIRouter
from datetime import datetime, timedelta
import random, math

router = APIRouter()

def gen_timeseries(base: float, variance: float, points: int = 24):
    return [
        {
            "t": f"{str(i).zfill(2)}:00",
            "v": round(max(0, base + (random.random() - 0.5) * variance), 2)
        }
        for i in range(points)
    ]

@router.get("/metrics")
async def get_metrics():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "network_health": round(random.uniform(92, 96), 1),
        "active_slices": 6,
        "avg_latency_ms": round(random.uniform(7.5, 10.2), 1),
        "connected_devices": random.randint(167800, 169200),
        "call_success_rate": round(random.uniform(96.5, 98.5), 1),
        "auth_success_rate": round(random.uniform(97.8, 99.1), 1),
        "threat_level": "MEDIUM",
        "threat_score": random.randint(55, 68),
        "ai_confidence": round(random.uniform(89, 95), 1),
        "twin_sync_pct": 99.8,
        "prediction_accuracy": 94.2,
    }

@router.get("/traffic")
async def get_traffic():
    """24-hour traffic timeseries."""
    return {
        "uplink_gbps": gen_timeseries(52, 30),
        "downlink_gbps": gen_timeseries(78, 42),
        "latency_ms": gen_timeseries(8.5, 4),
    }

@router.get("/radar")
async def get_radar():
    """Network health radar data."""
    return [
        {"metric": "Throughput",  "score": round(random.uniform(88, 96), 1)},
        {"metric": "Latency",     "score": round(random.uniform(84, 92), 1)},
        {"metric": "Reliability", "score": round(random.uniform(92, 98), 1)},
        {"metric": "Security",    "score": round(random.uniform(70, 80), 1)},
        {"metric": "AI Score",    "score": round(random.uniform(88, 95), 1)},
        {"metric": "Efficiency",  "score": round(random.uniform(80, 88), 1)},
    ]

@router.get("/ai-recommendations")
async def get_ai_recommendations():
    return [
        {"id": 1, "type": "optimize", "title": "Scale mMTC-IoT Slice",
         "desc": "Occupancy at 88%. Recommend +30% capacity allocation.", "confidence": 94, "priority": "high", "t": "2m ago"},
        {"id": 2, "type": "predict", "title": "Congestion Predicted — Edge-02",
         "desc": "Traffic spike forecast in 14 min. Pre-positioning resources.", "confidence": 87, "priority": "high", "t": "5m ago"},
        {"id": 3, "type": "security", "title": "Anomalous Auth Pattern",
         "desc": "Region MUM-03 shows 3.2× auth failure spike.", "confidence": 79, "priority": "medium", "t": "8m ago"},
        {"id": 4, "type": "maintain", "title": "gNB-003 Maintenance Due",
         "desc": "Predictive model flags hardware degradation in 48h.", "confidence": 92, "priority": "low", "t": "15m ago"},
    ]
