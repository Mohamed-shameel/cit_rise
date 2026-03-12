from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import json

from config.store import users_db, achievements_db
from services.ai_service import call_llama, parse

router = APIRouter()

class AvatarGenReq(BaseModel):
    student_id: str
    gender: Optional[str] = "male"
    force_regenerate: Optional[bool] = False

@router.post("/generate")
async def generate_avatar(req: AvatarGenReq):
    student = users_db.get(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    score = student.get("rise_score", 0)
    
    # Defaults and Tiers setup
    if score <= 100:
        tier, title = "Starter", "Seed"
        clotheType, clotheColor = "ShirtCrewNeck", "Gray01"
        accessoriesType, aura = "Blank", "none"
    elif score <= 200:
        tier, title = "Explorer", "Builder"
        clotheType, clotheColor = "Hoodie", "Blue03"
        accessoriesType, aura = "Round", "blue_glow"
    elif score <= 350:
        tier, title = "Innovator", "Catalyst"
        clotheType, clotheColor = "BlazerShirt", "Blue01"
        accessoriesType, aura = "Prescription01", "cyan_pulse"
    else:
        tier, title = "Pioneer", "Vanguard"
        clotheType, clotheColor = "BlazerSweater", "Black"
        accessoriesType, aura = "Kurt", "purple_crown"

    # Achievements / Graphic logic
    verified_achs = [a for a in achievements_db.values() if a.get("student_id") == req.student_id and a.get("verified")]
    ach_types = [a.get("type", "default") for a in verified_achs]
    
    graphicType = "Skull"
    if "hackathon" in ach_types: graphicType = "Diamond"
    elif "research" in ach_types: graphicType = "Hola"
    elif "startup" in ach_types: graphicType = "Rocket"
    elif "patent" in ach_types: graphicType = "Selena"
    elif "competition" in ach_types: graphicType = "Bear"
    elif "project" in ach_types: graphicType = "Bat"
    
    badge_map = {
        "hackathon": "🏆", "research": "📄", "startup": "🚀",
        "patent": "⭐", "competition": "🥇", "project": "💡", "certification": "✅"
    }
    earnedBadges = list(set([badge_map.get(t) for t in ach_types if badge_map.get(t)]))

    # Llama 3 Personalization Call
    sys_prompt = "You are generating avatar appearance settings for a student profile system. Return ONLY valid JSON."
    prompt = f"""Student details:
- Name: {student.get('name', 'Student')}
- Department: {student.get('department', 'CSE')}
- Skills: {', '.join(student.get('skills', []))}
- Interests: {', '.join(student.get('interests', []))}
- Gender: {req.gender}

Return ONLY valid JSON with exactly these fields:
{{
  "topType": one of [ShortHairShortFlat, ShortHairDreads01, LongHairStraight, LongHairCurvy, ShortHairShortWaved, LongHairBob, ShortHairTheCaesar, WinterHat1],
  "hairColor": one of [Black, Brown, Blonde, Auburn, Red, SilverGray],
  "skinColor": one of [Light, Yellow, Tanned, Brown, DarkBrown, Black],
  "facialHairType": one of [Blank, BeardLight, BeardMedium, MoustacheFancy] (use Blank if gender is female),
  "eyeType": one of [Default, Happy, Wink, Hearts, Side, Surprised],
  "eyebrowType": one of [Default, RaisedExcited, FlatNatural, UpDown],
  "mouthType": one of [Default, Smile, Twinkle, Tongue, Serious],
  "avatarStory": a single sentence (max 15 words) capturing this student's innovation identity based strictly on their skills and department.
}}"""
    
    raw = await call_llama(prompt, sys_prompt)
    ai_config = parse(raw, {
        "topType": "ShortHairShortFlat", "hairColor": "Black", "skinColor": "Brown",
        "facialHairType": "Blank", "eyeType": "Default", "eyebrowType": "Default",
        "mouthType": "Smile", "avatarStory": f"An innovative student from {student.get('department')} building the future."
    })

    avatar_config = {
        "clotheType": clotheType, "clotheColor": clotheColor,
        "accessoriesType": accessoriesType, "graphicType": graphicType,
        "tier": tier, "title": title, "aura": aura, "earnedBadges": earnedBadges,
        "topType": ai_config.get("topType", "ShortHairShortFlat"),
        "hairColor": ai_config.get("hairColor", "Black"),
        "skinColor": ai_config.get("skinColor", "Brown"),
        "facialHairType": ai_config.get("facialHairType", "Blank"),
        "eyeType": ai_config.get("eyeType", "Default"),
        "eyebrowType": ai_config.get("eyebrowType", "Default"),
        "mouthType": ai_config.get("mouthType", "Smile"),
        "avatarStory": ai_config.get("avatarStory", "Building the future."),
        "avatarStyle": "Circle",
        "gender": req.gender,
        "rise_score": score,
        "generated_at": datetime.utcnow().isoformat()
    }

    student["avatar_config"] = avatar_config
    student["avatar_generated_at"] = avatar_config["generated_at"]
    student["gender"] = req.gender

    return avatar_config

@router.get("/{student_id}")
async def get_avatar(student_id: str):
    student = users_db.get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    config = student.get("avatar_config")
    if config and student.get("avatar_generated_at"):
        gen_date = datetime.fromisoformat(student["avatar_generated_at"])
        if datetime.utcnow() - gen_date < timedelta(days=30):
            return config

    # Missing or expired - auto generate (using default male if not set)
    gender = student.get("gender", "male")
    return await generate_avatar(AvatarGenReq(student_id=student_id, gender=gender, force_regenerate=True))
