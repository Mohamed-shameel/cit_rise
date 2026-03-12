from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from config.store import mentors_db, users_db

router = APIRouter()

class MentorCreate(BaseModel):
    name: str; company: str; domain: str
    skills: List[str]=[]; bio: Optional[str]=""; linkedin: Optional[str]=""

class MentorUpdate(BaseModel):
    name: Optional[str]=None; company: Optional[str]=None; domain: Optional[str]=None
    skills: Optional[List[str]]=None; bio: Optional[str]=None; linkedin: Optional[str]=None
    available: Optional[bool]=None

@router.get("/")
async def list_mentors():
    return {"total":len(mentors_db),"mentors":list(mentors_db.values())}

@router.post("/add")
async def add_mentor(m: MentorCreate):
    mid = f"mentor_{uuid.uuid4().hex[:8]}"
    mentors_db[mid] = {"mentor_id":mid, **m.model_dump(), "available":True}
    return {"message":"Added","mentor":mentors_db[mid]}

@router.put("/{mentor_id}")
async def update_mentor(mentor_id: str, update: MentorUpdate):
    if mentor_id not in mentors_db:
        raise HTTPException(404, "Mentor not found")
    m = mentors_db[mentor_id]
    for k, v in update.model_dump(exclude_none=True).items(): 
        m[k] = v
    return {"message": "Mentor updated", "mentor": m}

@router.delete("/{mentor_id}")
async def delete_mentor(mentor_id: str):
    if mentor_id not in mentors_db:
        raise HTTPException(404, "Mentor not found")
    del mentors_db[mentor_id]
    return {"message": "Mentor removed successfully"}

@router.get("/recommend/{student_id}")
async def recommend(student_id: str):
    s = users_db.get(student_id)
    if not s: raise HTTPException(404,"Student not found")
    student_skills = set(sk.lower() for sk in s.get("skills",[]))
    scored = []
    for m in mentors_db.values():
        mentor_skills = set(sk.lower() for sk in m.get("skills",[]))
        match = len(student_skills & mentor_skills)
        scored.append({**m,"match_score":round(match/max(len(student_skills),1)*100)})
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return {"student_id":student_id,"recommended_mentors":scored[:4]}
