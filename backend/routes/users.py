from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid, io

from config.store import users_db
from services.ai_service import generate_student_profile, calculate_rise_score, regenerate_student_profile

router = APIRouter()

class UserCreate(BaseModel):
    name: str; email: str; role: str = "student"; department: str
    year: Optional[int] = None; skills: List[str] = []; interests: List[str] = []
    github: Optional[str] = None; linkedin: Optional[str] = None

class UserUpdate(BaseModel):
    skills: Optional[List[str]] = None; interests: Optional[List[str]] = None
    github: Optional[str] = None; linkedin: Optional[str] = None
    department: Optional[str] = None; year: Optional[int] = None

@router.post("/create")
async def create_user(user: UserCreate):
    uid = f"user_{uuid.uuid4().hex[:8]}"
    users_db[uid] = {"user_id":uid, **user.model_dump(), "rise_score":0,
        "rise_score_breakdown":{}, "rise_score_meta":{}, "ai_profile_summary":None,
        "career_roadmap":None, "created_at":datetime.utcnow().isoformat()}
    return {"message":"User created","user_id":uid,"user":users_db[uid]}

@router.get("/")
async def list_users(role: Optional[str]=None, department: Optional[str]=None):
    users = list(users_db.values())
    if role: users = [u for u in users if u.get("role")==role]
    if department: users = [u for u in users if u.get("department")==department]
    return {"total":len(users),"users":users}

@router.get("/{user_id}")
async def get_user(user_id: str):
    u = users_db.get(user_id)
    if not u: raise HTTPException(404, "User not found")
    return u

@router.put("/{user_id}/update")
async def update_user(user_id: str, update: UserUpdate):
    u = users_db.get(user_id)
    if not u: raise HTTPException(404, "User not found")
    for k,v in update.model_dump(exclude_none=True).items(): u[k] = v
    return {"message":"Updated","user":u}

@router.delete("/{student_id}")
async def delete_user(student_id: str, admin_user_id: str = "admin"):
    # Simplified admin check
    if student_id not in users_db:
        raise HTTPException(404, "Student not found")
    del users_db[student_id]
    return {"message": "Student deleted successfully"}

class ScoreOverride(BaseModel):
    rise_score: int

@router.put("/admin/students/{student_id}/score")
async def override_score(student_id: str, data: ScoreOverride):
    if student_id not in users_db:
        raise HTTPException(404, "Student not found")
    if not (0 <= data.rise_score <= 500):
        raise HTTPException(400, "Score must be between 0 and 500")
    users_db[student_id]["rise_score"] = data.rise_score
    return {"message": "Score updated successfully", "new_score": data.rise_score}

class RegenerateReq(BaseModel):
    student_id: str

@router.post("/regenerate-profile")
async def regenerate_profile(req: RegenerateReq):
    student = users_db.get(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    
    new_data = await regenerate_student_profile(student)
    
    student["ai_profile_summary"] = new_data.get("profile_summary", student.get("ai_profile_summary"))
    student["suggested_roles"] = new_data.get("suggested_roles", student.get("suggested_roles"))
    
    return {
        "message": "Profile regenerated", 
        "ai_profile_summary": student["ai_profile_summary"], 
        "suggested_roles": student["suggested_roles"]
    }

@router.get("/{user_id}/xp")
async def get_xp(user_id: str):
    u = users_db.get(user_id)
    if not u: raise HTTPException(404, "User not found")
    xp = u.get("xp", 0)
    level = 1 + xp // 100
    labels = {1:"Newcomer", 2:"Explorer", 3:"Innovator", 4:"Pioneer", 5:"Legend"}
    label = labels.get(min(level, 5), "Legend")
    return {"user_id": user_id, "xp": xp, "level": min(level, 5), "level_label": label,
            "xp_to_next": (min(level, 5) * 100) - xp if level < 5 else 0}


@router.post("/ai-profile-from-resume")
async def ai_profile_from_resume(
    resume_file: UploadFile = File(...),
    github_username: Optional[str] = Form(None),
    email: Optional[str] = Form(None)
):
    import pypdfium2 as pdfium
    if not (resume_file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported.")
    data = await resume_file.read()
    text = ""
    try:
        pdf = pdfium.PdfDocument(io.BytesIO(data))
        for i in range(len(pdf)):
            page = pdf[i]
            textpage = page.get_textpage()
            t = textpage.get_text_range()
            if t: text += t + "\n"
    except Exception as e:
        raise HTTPException(400, f"Could not read PDF: {e}")
    if not text.strip():
        raise HTTPException(400, "No extractable text found. Use a PDF with selectable text.")
    profile = await generate_student_profile(text, github_username)
    uid = f"user_{uuid.uuid4().hex[:8]}"
    rec = {"user_id":uid,"email":email or f"{profile.get('name','student').lower().replace(' ','.')}@citchennai.net",
        "role":"student","name":profile.get("name","Student"),"department":profile.get("department","CSE"),
        "year":profile.get("year",1),"skills":profile.get("skills",[]),"interests":profile.get("interests",[]),
        "github":github_username,"linkedin":None,"ai_profile_summary":profile.get("profile_summary"),
        "innovation_potential":profile.get("innovation_potential"),"suggested_roles":profile.get("suggested_roles",[]),
        "strengths":profile.get("strengths",[]),"rise_score":0,"rise_score_breakdown":{},"career_roadmap":None,
        "created_at":datetime.utcnow().isoformat(),"profile_source":"pdf_upload"}
    score = await calculate_rise_score(rec, [])
    rec["rise_score"] = score.get("total_score",0)
    rec["rise_score_breakdown"] = score.get("breakdown",{})
    rec["rise_score_meta"] = {"percentile":score.get("percentile"),"reasoning":score.get("score_reasoning"),
        "badge":score.get("badge"),"improvement_areas":score.get("improvement_areas",[])}
    users_db[uid] = rec
    return {"message":"Profile generated from PDF","user_id":uid,"ai_extracted":profile,"initial_rise_score":score,"profile":rec}
