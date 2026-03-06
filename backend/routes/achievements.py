from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

from config.store import users_db, achievements_db
from services.ai_service import calculate_rise_score

router = APIRouter()
TYPES = ["hackathon","project","research","startup","patent","certification","competition"]

class AchCreate(BaseModel):
    student_id: str; title: str; type: str
    description: Optional[str]=""; date: Optional[str]=None; certificate_url: Optional[str]=None

@router.post("/add")
async def add_achievement(a: AchCreate):
    if a.student_id not in users_db: raise HTTPException(404,"Student not found")
    if a.type not in TYPES: raise HTTPException(400,f"Type must be one of: {TYPES}")
    aid = f"ach_{uuid.uuid4().hex[:8]}"
    rec = {"achievement_id":aid,"student_id":a.student_id,"title":a.title,"type":a.type,
        "description":a.description,"date":a.date or datetime.utcnow().strftime("%Y-%m-%d"),
        "certificate_url":a.certificate_url,"verified":False,"created_at":datetime.utcnow().isoformat()}
    achievements_db[aid] = rec
    student = users_db[a.student_id]
    all_ach = [x for x in achievements_db.values() if x["student_id"]==a.student_id]
    score = await calculate_rise_score(student, all_ach)
    student["rise_score"] = score.get("total_score", student["rise_score"])
    student["rise_score_breakdown"] = score.get("breakdown",{})
    student["rise_score_meta"] = {"percentile":score.get("percentile"),"reasoning":score.get("score_reasoning"),
        "badge":score.get("badge"),"improvement_areas":score.get("improvement_areas",[])}
    return {"message":"Achievement added, score recalculated","achievement":rec,"updated_rise_score":score}

@router.get("/{student_id}")
async def get_achievements(student_id: str):
    if student_id not in users_db: raise HTTPException(404,"Student not found")
    achs = [a for a in achievements_db.values() if a["student_id"]==student_id]
    return {"student_id":student_id,"total":len(achs),"achievements":achs}

@router.put("/{achievement_id}/verify")
async def verify(achievement_id: str):
    a = achievements_db.get(achievement_id)
    if not a: raise HTTPException(404,"Achievement not found")
    a["verified"] = True; a["verified_at"] = datetime.utcnow().isoformat()
    return {"message":"Verified","achievement":a}

@router.delete("/{achievement_id}/reject")
async def reject(achievement_id: str, reason: Optional[str]="Does not meet criteria"):
    a = achievements_db.get(achievement_id)
    if not a: raise HTTPException(404,"Achievement not found")
    a["verified"]=False; a["rejected"]=True; a["rejection_reason"]=reason
    return {"message":"Rejected","achievement":a}

@router.get("/")
async def list_all(verified: Optional[bool]=None):
    achs = list(achievements_db.values())
    if verified is not None: achs = [a for a in achs if a.get("verified")==verified]
    return {"total":len(achs),"achievements":achs}
