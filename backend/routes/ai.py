from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from config.store import users_db, achievements_db, user_opportunities, opportunities_db, daily_challenges_db
from services.ai_service import generate_career_roadmap, calculate_rise_score, chat_with_ai, generate_admin_insights, generate_daily_challenge
from services.opportunity_scoring import update_rise_score_for_opportunity, generate_opportunity_insights

router = APIRouter()

class Req(BaseModel):
    student_id: str

class ChatReq(BaseModel):
    student_id: str
    question: str
    current_page: Optional[str] = ""

class NodeUpdateReq(BaseModel):
    student_id: str
    node_id: str
    status: str  # "completed" | "in_progress" | "pending"

class ChallengeAnswerReq(BaseModel):
    answer: str  # "A", "B", "C", or "D"

@router.post("/career-roadmap")
async def career_roadmap(req: Req):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    achs = [a for a in achievements_db.values() if a["student_id"]==req.student_id]
    roadmap = await generate_career_roadmap(s, achs)
    s["career_roadmap"] = roadmap
    return {"student_id":req.student_id,"roadmap":roadmap,"generated_by":"Llama AI"}

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
    hist = s.setdefault("score_history", [])
    hist.append({"score": s["rise_score"], "date": datetime.utcnow().strftime("%Y-%m-%d")})
    s["score_history"] = hist[-30:]
    return {"student_id":req.student_id,"rise_score_analysis":score}

@router.post("/recalculate-score-with-opportunities")
async def recalculate_score_with_opportunities(req: Req):
    """
    Recalculate RISE score including opportunity participation impact
    """
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404, "Student not found")
    
    # Get user's achievements
    achs = [a for a in achievements_db.values() if a["student_id"] == req.student_id]
    
    # Get user's opportunities
    user_opps = [uo for uo in user_opportunities.values() if uo.get("user_id") == req.student_id]
    
    # Calculate base RISE score
    base_score = await calculate_rise_score(s, achs)
    
    # Apply opportunity-based adjustments
    s_updated, opportunity_boost = update_rise_score_for_opportunity(s, user_opps, opportunities_db)
    
    # Calculate final score
    final_total = base_score.get("total_score", 0) + opportunity_boost
    
    # Generate opportunity insights for reasoning
    opp_insights = generate_opportunity_insights(user_opps, opportunities_db)
    
    # Update user record
    extended_breakdown = base_score.get("breakdown", {})
    extended_breakdown["opportunity_participation"] = opportunity_boost
    
    s["rise_score"] = final_total
    s["rise_score_breakdown"] = extended_breakdown
    s["rise_score_meta"] = {
        "percentile": base_score.get("percentile"),
        "reasoning": f"{base_score.get('score_reasoning', '')} Opportunity engagement: {opp_insights}",
        "badge": base_score.get("badge"),
        "improvement_areas": base_score.get("improvement_areas", [])
    }
    
    return {
        "student_id": req.student_id,
        "base_score": base_score.get("total_score", 0),
        "opportunity_boost": opportunity_boost,
        "final_rise_score": final_total,
        "rise_score_analysis": s["rise_score_meta"],
        "opportunity_contribution": s_updated.get("opportunity_contribution", {})
    }

@router.post("/chat")
async def chat(req: ChatReq):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    answer = await chat_with_ai(req.question, s, req.current_page or "")
    return {"student_id":req.student_id,"question":req.question,"answer":answer}


@router.post("/roadmap/update-node")
async def update_roadmap_node(req: NodeUpdateReq):
    s = users_db.get(req.student_id)
    if not s: raise HTTPException(404,"Student not found")
    roadmap = s.get("career_roadmap")
    if not roadmap: raise HTTPException(400,"No roadmap found. Generate one first.")
    node_statuses = s.setdefault("roadmap_node_statuses", {})
    node_statuses[req.node_id] = req.status
    return {"student_id": req.student_id, "node_id": req.node_id, "status": req.status}


@router.get("/daily-challenge/{student_id}")
async def get_daily_challenge(student_id: str):
    s = users_db.get(student_id)
    if not s: raise HTTPException(404,"Student not found")
    today = date.today().isoformat()
    existing = daily_challenges_db.get(student_id)
    if existing and existing.get("date") == today:
        safe = {k: v for k, v in existing.items() if k != "correct"}
        return safe
    challenge = await generate_daily_challenge(s)
    record = {
        "student_id": student_id,
        "date": today,
        "question": challenge.get("question"),
        "options": challenge.get("options", []),
        "correct": challenge.get("correct"),
        "explanation": challenge.get("explanation", ""),
        "answered": False,
        "answer_given": None,
        "xp_earned": 0,
    }
    daily_challenges_db[student_id] = record
    return {k: v for k, v in record.items() if k != "correct"}


@router.post("/daily-challenge/{student_id}/answer")
async def answer_daily_challenge(student_id: str, req: ChallengeAnswerReq):
    s = users_db.get(student_id)
    if not s: raise HTTPException(404,"Student not found")
    today = date.today().isoformat()
    challenge = daily_challenges_db.get(student_id)
    if not challenge or challenge.get("date") != today:
        raise HTTPException(400,"No challenge for today. Fetch it first.")
    if challenge.get("answered"):
        return {"already_answered": True, "correct": challenge["answer_given"] == challenge["correct"],
                "correct_answer": challenge["correct"], "explanation": challenge["explanation"], "xp_earned": 0}
    is_correct = req.answer.upper() == challenge["correct"].upper()
    xp = 5 if is_correct else 2
    challenge["answered"] = True
    challenge["answer_given"] = req.answer.upper()
    challenge["xp_earned"] = xp
    s["xp"] = s.get("xp", 0) + xp
    return {
        "correct": is_correct,
        "your_answer": req.answer.upper(),
        "correct_answer": challenge["correct"],
        "explanation": challenge["explanation"],
        "xp_earned": xp,
        "total_xp": s["xp"],
    }

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
