from fastapi import APIRouter
from typing import Optional
from config.store import users_db, achievements_db, opportunities_db

router = APIRouter()


@router.get("/leaderboard")
async def get_leaderboard(department: Optional[str] = None):
    students = [u for u in users_db.values() if u.get("role") == "student"]
    if department:
        students = [s for s in students if s.get("department") == department]

    sorted_students = sorted(students, key=lambda x: x.get("rise_score", 0), reverse=True)
    departments = sorted(set(u.get("department", "") for u in users_db.values() if u.get("role") == "student"))

    leaderboard = []
    for rank, student in enumerate(sorted_students[:20], 1):
        prev_score = None
        history = student.get("score_history", [])
        if len(history) >= 2:
            prev_score = history[-2]["score"]
        delta = (student.get("rise_score", 0) - prev_score) if prev_score is not None else None

        leaderboard.append({
            "rank": rank,
            "user_id": student["user_id"],
            "name": student["name"],
            "department": student.get("department", ""),
            "rise_score": student.get("rise_score", 0),
            "badge": student.get("rise_score_meta", {}).get("badge", "Starter"),
            "avatar": student.get("avatar", {}),
            "delta": delta,
        })

    return {
        "total_students": len(students),
        "departments": departments,
        "leaderboard": leaderboard,
    }

@router.get("/dashboard")
async def dashboard():
    students = [u for u in users_db.values() if u.get("role")=="student"]
    pending = [a for a in achievements_db.values() if not a.get("verified") and not a.get("rejected")]
    depts = {}
    for s in students:
        d = s.get("department","Unknown"); depts[d] = depts.get(d,0)+1
    top = sorted(students, key=lambda x: x.get("rise_score",0), reverse=True)[:10]
    return {"stats":{"total_students":len(students),"total_achievements":len(achievements_db),
        "pending_verifications":len(pending),"total_opportunities":len(opportunities_db),
        "average_rise_score":sum(s.get("rise_score",0) for s in students)//max(len(students),1)},
        "department_distribution":depts,
        "top_innovators":[{"name":s["name"],"department":s.get("department"),"rise_score":s.get("rise_score",0),
            "badge":s.get("rise_score_meta",{}).get("badge","—"),"user_id":s["user_id"]} for s in top],
        "pending_achievements":pending}
