from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.store import users_db, achievements_db
from services.ai_service import generate_career_roadmap, calculate_rise_score, chat_with_ai, generate_admin_insights

router = APIRouter()

class Req(BaseModel):
    student_id: str

class ChatReq(BaseModel):
    student_id: str; question: str

@router.post("/career-roadmap")
async def career_roadmap(req: Req):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    achs = [a for a in achievements_db.values() if a["student_id"]==req.student_id]
    roadmap = await generate_career_roadmap(s, achs)
    s["career_roadmap"] = roadmap
    return {"student_id":req.student_id,"roadmap":roadmap,"generated_by":"Gemini AI"}

@router.post("/recalculate-score")
async def recalculate_score(req: Req):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    achs = [a for a in achievements_db.values() if a["student_id"]==req.student_id]
    score = await calculate_rise_score(s, achs)
    s["rise_score"] = score.get("total_score",0)
    s["rise_score_breakdown"] = score.get("breakdown",{})
    s["rise_score_meta"] = {"percentile":score.get("percentile"),"reasoning":score.get("score_reasoning"),
        "badge":score.get("badge"),"improvement_areas":score.get("improvement_areas",[])}
    return {"student_id":req.student_id,"rise_score_analysis":score}

@router.post("/chat")
async def chat(req: ChatReq):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    answer = await chat_with_ai(req.question, s)
    return {"student_id":req.student_id,"question":req.question,"answer":answer}

@router.get("/admin-insights")
async def admin_insights():
    insights = await generate_admin_insights(users_db, achievements_db)
    students = [u for u in users_db.values() if u.get("role")=="student"]
    top = sorted(students, key=lambda x: x.get("rise_score",0), reverse=True)[:5]
    return {"ai_insights":insights,"raw_stats":{
        "total_students":len(students),"total_achievements":len(achievements_db),
        "average_rise_score":sum(s.get("rise_score",0) for s in students)//max(len(students),1),
        "top_innovators":[{"name":s["name"],"department":s.get("department"),"rise_score":s.get("rise_score",0),
            "badge":s.get("rise_score_meta",{}).get("badge","—")} for s in top]}}
