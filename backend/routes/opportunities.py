from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from config.store import opportunities_db

router = APIRouter()

class OppCreate(BaseModel):
    title: str; description: str; domain: str
    deadline: Optional[str]=None; type: str = "internship"

@router.get("/")
async def list_opps(type: Optional[str]=None):
    opps = list(opportunities_db.values())
    if type: opps = [o for o in opps if o.get("type")==type]
    return {"total":len(opps),"opportunities":opps}

@router.post("/create")
async def create_opp(o: OppCreate):
    oid = f"opp_{uuid.uuid4().hex[:8]}"
    opportunities_db[oid] = {"opportunity_id":oid, **o.model_dump(),
        "posted_by":"admin","created_at":datetime.utcnow().isoformat()}
    return {"message":"Created","opportunity":opportunities_db[oid]}

@router.delete("/{opp_id}")
async def delete_opp(opp_id: str):
    if opp_id not in opportunities_db: raise HTTPException(404,"Not found")
    del opportunities_db[opp_id]
    return {"message":"Deleted"}
