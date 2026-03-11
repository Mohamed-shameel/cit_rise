from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from config.store import users_db

router = APIRouter()

class AvatarGenReq(BaseModel):
    student_id: str
    gender: str = "male"  # "male" or "female"

def _build_avatar_url(student_id: str, gender: str, score: int) -> str:
    tier = (
        "pioneer" if score >= 350 else
        "innovator" if score >= 200 else
        "explorer" if score >= 100 else
        "starter"
    )
    if gender == "female":
        top = "longHairStraight"
        clothing = "blazerAndShirt" if tier in ("pioneer", "innovator") else "hoodie"
    else:
        top = "shortHairShortWaved"
        clothing = "blazerAndShirt" if tier in ("pioneer", "innovator") else "hoodie"

    accessories_map = {
        "pioneer":  "kurt",
        "innovator": "prescription01",
        "explorer": "",
        "starter":  "",
    }
    accessories = accessories_map[tier]
    accessory_param = f"&accessories[]={accessories}" if accessories else ""

    seed = f"{student_id}_{gender}_{tier}"
    url = (
        f"https://api.dicebear.com/7.x/avataaars/svg"
        f"?seed={seed}&top[]={top}&clothing[]={clothing}{accessory_param}"
    )
    return url, tier


@router.post("/generate")
async def generate_avatar(req: AvatarGenReq):
    student = users_db.get(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    score = student.get("rise_score", 0)
    url, tier = _build_avatar_url(req.student_id, req.gender, score)

    student["avatar"] = {
        "url": url,
        "gender": req.gender,
        "tier": tier,
        "generated_at": datetime.utcnow().isoformat(),
    }
    return {"student_id": req.student_id, "avatar": student["avatar"]}


@router.get("/{student_id}")
async def get_avatar(student_id: str):
    student = users_db.get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    avatar = student.get("avatar")
    if not avatar:
        score = student.get("rise_score", 0)
        url, tier = _build_avatar_url(student_id, "male", score)
        avatar = {"url": url, "gender": "male", "tier": tier}

    return {"student_id": student_id, "avatar": avatar}
