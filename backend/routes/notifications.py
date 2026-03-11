from fastapi import APIRouter, HTTPException
from datetime import date

from config.store import users_db, opportunities_db, daily_challenges_db

router = APIRouter()


@router.get("/{student_id}")
async def get_notifications(student_id: str):
    student = users_db.get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    notifications = []
    today = date.today().isoformat()

    # 1. Score stale — no score history means never calculated
    history = student.get("score_history", [])
    if not history:
        notifications.append({
            "id": "score_stale",
            "type": "action",
            "title": "Calculate your RISE Score",
            "message": "Add achievements and calculate your RISE score to get ranked.",
            "icon": "📊",
            "page": "score",
        })

    # 2. Daily challenge ready
    challenge = daily_challenges_db.get(student_id)
    if not challenge or challenge.get("date") != today:
        notifications.append({
            "id": "daily_challenge",
            "type": "challenge",
            "title": "Daily Challenge Ready",
            "message": "Answer today's question and earn +5 XP.",
            "icon": "⚡",
            "page": "dashboard",
        })
    elif challenge.get("date") == today and not challenge.get("answered"):
        notifications.append({
            "id": "daily_challenge_pending",
            "type": "challenge",
            "title": "Challenge Unanswered",
            "message": "You still have today's challenge — answer before midnight!",
            "icon": "⚡",
            "page": "dashboard",
        })

    # 3. New opportunities matching department
    dept = student.get("department", "")
    dept_opps = [o for o in opportunities_db.values() if dept in o.get("department_fit", [])]
    if dept_opps:
        notifications.append({
            "id": "new_opps",
            "type": "opportunity",
            "title": f"{len(dept_opps)} Opportunities for You",
            "message": f"Opportunities matching {dept} are available.",
            "icon": "🎯",
            "page": "opportunities",
        })

    # 4. No career roadmap
    if not student.get("career_roadmap"):
        notifications.append({
            "id": "no_roadmap",
            "type": "info",
            "title": "Generate Your Career Roadmap",
            "message": "Get a personalized AI-powered career plan.",
            "icon": "🗺️",
            "page": "roadmap",
        })

    # 5. No GitHub analysis
    if not student.get("github_analysis"):
        notifications.append({
            "id": "no_github",
            "type": "info",
            "title": "Connect GitHub Profile",
            "message": "Analyze your GitHub to enrich your RISE score.",
            "icon": "🐙",
            "page": "careernav",
        })

    return {
        "student_id": student_id,
        "count": len(notifications),
        "notifications": notifications,
    }
