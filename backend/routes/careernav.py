from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.store import users_db, achievements_db
from services.ai_service import analyze_github, analyze_leetcode, calculate_rise_score

router = APIRouter()

class GHReq(BaseModel):
    username: str; student_id: Optional[str]=None

class LCReq(BaseModel):
    username: str; student_id: Optional[str]=None

@router.post("/github")
async def github_analysis(req: GHReq):
    result = await analyze_github(req.username)
    if "error" in result: raise HTTPException(404, result["error"])
    if req.student_id and req.student_id in users_db:
        s = users_db[req.student_id]; ai = result["ai_analysis"]
        s["skills"] = list(set(s.get("skills",[])) | set(ai.get("detected_skills",[])))
        s["github_analysis"] = {"username":req.username,"developer_level":ai.get("developer_level"),
            "primary_domain":ai.get("primary_domain"),"open_source_score":ai.get("open_source_score"),
            "career_readiness":ai.get("career_readiness"),"summary":ai.get("github_summary"),
            "total_stars":result["raw"].get("total_stars",0),"public_repos":result["raw"].get("public_repos",0)}
        achs = [a for a in achievements_db.values() if a["student_id"]==req.student_id]
        score = await calculate_rise_score(s, achs)
        s["rise_score"] = score.get("total_score", s["rise_score"])
        result["profile_enriched"]=True; result["new_rise_score"]=score.get("total_score")
    return {"username":req.username,"github_url":f"https://github.com/{req.username}",**result}

@router.post("/leetcode")
async def leetcode_analysis(req: LCReq):
    result = await analyze_leetcode(req.username)
    if "error" in result: raise HTTPException(404, result["error"])
    if req.student_id and req.student_id in users_db:
        s = users_db[req.student_id]; ai = result["ai_analysis"]
        s["leetcode_analysis"] = {"username":req.username,"dsa_level":ai.get("dsa_level"),
            "interview_readiness":ai.get("interview_readiness"),
            "solved_total":result["raw"]["solved"]["total"],"company_targets":ai.get("company_targets",[])}
        result["profile_enriched"]=True
    return {"username":req.username,"leetcode_url":f"https://leetcode.com/{req.username}",**result}
