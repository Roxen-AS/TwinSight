"""Incident Management API"""
from fastapi import APIRouter
router = APIRouter()

INCIDENTS = [
    {"id": "INC-4421","sev": "critical","title": "Volumetric DDoS — Core Network","status": "active","t": "12m ago","ai": False},
    {"id": "INC-4418","sev": "high",    "title": "Slice Overload — mMTC-IoT",     "status": "investigating","t": "28m ago","ai": True},
    {"id": "INC-4415","sev": "medium",  "title": "Auth Failure Spike — MUM-03",   "status": "resolved","t": "1h ago","ai": True},
    {"id": "INC-4410","sev": "low",     "title": "gNB-007 Signal Degradation",    "status": "resolved","t": "3h ago","ai": True},
]

@router.get("/")
async def list_incidents():
    return INCIDENTS

@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    inc = next((x for x in INCIDENTS if x["id"] == incident_id), None)
    if not inc:
        from fastapi import HTTPException
        raise HTTPException(404, "Incident not found")
    return inc

@router.post("/{incident_id}/resolve")
async def resolve_incident(incident_id: str):
    for inc in INCIDENTS:
        if inc["id"] == incident_id:
            inc["status"] = "resolved"
            return {"status": "resolved", "id": incident_id}
    from fastapi import HTTPException
    raise HTTPException(404, "Incident not found")
