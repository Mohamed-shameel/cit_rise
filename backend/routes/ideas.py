"""
Ideas Submission System Routes
Allows students to submit innovation ideas, get AI analysis, and admins to review
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import csv
import io

from config.store import ideas_db, idea_comments_db, idea_submissions_log, mentors_db, users_db
from services.ai_service import analyze_idea
from services.opportunity_scoring import adjust_rise_score_for_idea

router = APIRouter()

# Pydantic models
class IdeaSubmit(BaseModel):
    title: str
    description: str
    optional_files: str = None  # For future file upload

class IdeaUpdate(BaseModel):
    title: str = None
    description: str = None
    category: str = None

class IdeaReview(BaseModel):
    status: str  # 'reviewed', 'selected', 'rejected'
    admin_comment: str = ""
    mentor_assignment: str = None

class CommentAdd(BaseModel):
    comment: str

class StudentIdeaSubmit(BaseModel):
    title: str
    description: str
    student_id: str = "student_demo"

# Helper: Check if user is admin (simplified for demo)
def get_current_user(user_id: str = None):
    # In real app, extract from JWT token
    # For now, accept user_id from header or assume logged-in
    return {"user_id": user_id or "student_demo", "role": "student"}

def get_admin_user(user_id: str = None):
    # Simplified: any user with "admin" in email or hardcoded
    user = get_current_user(user_id)
    if user["user_id"] not in users_db or users_db[user["user_id"]].get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# Helper: Generate idea ID
def gen_idea_id():
    return str(uuid.uuid4())

# ============== STUDENT ENDPOINTS ==============

@router.post("/submit")
async def student_submit_idea(data: StudentIdeaSubmit):
    """
    Student submits an idea in-app. AI instantly scores it.
    """
    if data.student_id not in users_db:
        raise HTTPException(status_code=404, detail="Student not found")
    if len(data.title.strip()) < 5:
        raise HTTPException(status_code=400, detail="Title must be at least 5 characters")
    if len(data.description.strip()) < 20:
        raise HTTPException(status_code=400, detail="Description must be at least 20 characters")

    try:
        ai_result = await analyze_idea(data.title, data.description)
    except Exception as e:
        ai_result = {
            "category": "General Innovation",
            "feasibility_score": 55,
            "mentor_suggestions": list(mentors_db.keys())[:2],
            "feasibility_reasoning": "Could not analyze — manual review needed.",
            "implementation_complexity": "Medium",
            "potential_impact": "Medium",
            "suggested_first_steps": ["Research similar projects", "Draft an MVP", "Find a mentor"],
        }

    idea_id = gen_idea_id()
    idea = {
        "id": idea_id,
        "student_id": data.student_id,
        "title": data.title.strip()[:100],
        "description": data.description.strip(),
        "category": ai_result.get("category", "General Innovation"),
        "feasibility_score": ai_result.get("feasibility_score", 55),
        "mentor_suggestions": ai_result.get("mentor_suggestions", []),
        "status": "pending",
        "submitted_at": datetime.utcnow().isoformat(),
        "reviewed_at": None,
        "qr_code_url": "",
        "rise_score_impact": 0,
        "ai_analysis": ai_result,
    }

    ideas_db[idea_id] = idea
    idea_comments_db[idea_id] = []

    student = users_db[data.student_id]
    student["xp"] = student.get("xp", 0) + 10

    idea_submissions_log["total"] = len(ideas_db)
    cat = idea["category"]
    idea_submissions_log["categories"][cat] = idea_submissions_log["categories"].get(cat, 0) + 1

    return {
        "success": True,
        "idea_id": idea_id,
        "idea": idea,
        "ai_analysis": ai_result,
        "message": "Idea submitted and AI-analyzed! Admin will review shortly.",
    }


@router.get("/my-ideas")
def get_my_ideas(user_id: str = "student_demo"):
    """
    Get all ideas submitted by current student
    Returns: list of ideas with status
    """
    student_ideas = [idea for idea in ideas_db.values() if idea["student_id"] == user_id]
    
    return {
        "total": len(student_ideas),
        "ideas": sorted(student_ideas, key=lambda x: x["submitted_at"], reverse=True)
    }

@router.get("/{idea_id}")
def get_idea_detail(idea_id: str, user_id: str = "student_demo"):
    """
    Get detailed view of a single idea (only own ideas or admin)
    """
    idea = ideas_db.get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Check access
    if idea["student_id"] != user_id and user_id not in [u for u in users_db.values() if u.get("role") == "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    comments = idea_comments_db.get(idea_id, [])
    
    return {
        "idea": idea,
        "comments": comments,
        "mentor_details": [mentors_db.get(m, {}) for m in idea.get("mentor_suggestions", [])]
    }

# ============== ADMIN ENDPOINTS ==============

@router.get("/admin/list")
def admin_list_ideas(
    status: str = None,
    category: str = None,
    page: int = 1,
    limit: int = 20
):
    """
    Admin endpoint: List all ideas with filtering
    Filters: status (pending, reviewed, selected, rejected), category
    """
    ideas_list = list(ideas_db.values())
    
    # Apply filters
    if status:
        ideas_list = [i for i in ideas_list if i["status"] == status]
    if category:
        ideas_list = [i for i in ideas_list if i["category"] == category]
    
    # Sort by submitted date (newest first)
    ideas_list = sorted(ideas_list, key=lambda x: x["submitted_at"], reverse=True)
    
    # Pagination
    start = (page - 1) * limit
    paginated = ideas_list[start:start + limit]
    
    return {
        "total": len(ideas_list),
        "page": page,
        "limit": limit,
        "ideas": paginated,
        "analytics": idea_submissions_log
    }

@router.post("/admin/import-csv")
async def import_ideas_csv(file: UploadFile = File(...), admin_user_id: str = "admin"):
    """
    Admin imports ideas from a Google Forms CSV
    """
    _ = get_admin_user(admin_user_id) 
    
    try:
        content = await file.read()
        decoded = content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(e)}")
        
    imported_count = 0
    for row in reader:
        keys = {k.lower().strip(): k for k in row.keys() if k}
        
        # Heuristics to find columns
        title_key = next((keys[k] for k in keys if "title" in k or "idea" in k or "name" in k), None)
        desc_key = next((keys[k] for k in keys if "desc" in k or "detail" in k or "explain" in k), None)
        student_key = next((keys[k] for k in keys if "email" in k or "student" in k or "roll" in k or "id" in k), None)
        
        if not title_key and not desc_key:
            cols = list(row.keys())
            if len(cols) >= 2:
                title_key = cols[1]
                desc_key = cols[2] if len(cols) > 2 else cols[1]
                
        title = row.get(title_key, "Unknown Title") if title_key else "Unknown Title"
        desc = row.get(desc_key, "No description") if desc_key else "No description"
        student_id = row.get(student_key, "student_demo") if student_key else "student_demo"
        
        # AI Analysis
        try:
            ai_analysis = await analyze_idea(title, desc)
        except Exception as e:
            ai_analysis = {
                "category": "General Innovation",
                "feasibility_score": 50,
                "mentor_suggestions": list(mentors_db.keys())[:2] if mentors_db else [],
                "error": str(e)
            }
            
        idea_id = gen_idea_id()
        idea = {
            "id": idea_id,
            "student_id": student_id,
            "title": title[:100], # max 100 char title
            "description": desc,
            "category": ai_analysis.get("category", "General Innovation"),
            "feasibility_score": ai_analysis.get("feasibility_score", 50),
            "mentor_suggestions": ai_analysis.get("mentor_suggestions", []),
            "status": "pending",
            "submitted_at": datetime.utcnow().isoformat(),
            "reviewed_at": None,
            "qr_code_url": "", # Google form static QR
            "rise_score_impact": 0
        }
        
        ideas_db[idea_id] = idea
        idea_comments_db[idea_id] = []
        imported_count += 1
        
        idea_submissions_log["total"] = len(ideas_db)
        cat = idea["category"]
        idea_submissions_log["categories"][cat] = idea_submissions_log["categories"].get(cat, 0) + 1

    return {"success": True, "imported": imported_count, "message": f"Successfully imported and analyzed {imported_count} ideas"}

@router.put("/{idea_id}")
def update_idea(idea_id: str, data: IdeaUpdate):
    idea = ideas_db.get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.get("status") != "pending":
        raise HTTPException(status_code=400, detail="Cannot edit scored/reviewed ideas")
    
    for k, v in data.model_dump(exclude_none=True).items():
        idea[k] = v
        
    return {"message": "Idea updated successfully", "idea": idea}

@router.delete("/{idea_id}")
def delete_idea(idea_id: str, admin_user_id: str = "admin"):
    _ = get_admin_user(admin_user_id)
    if idea_id not in ideas_db:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    del ideas_db[idea_id]
    if idea_id in idea_comments_db:
        del idea_comments_db[idea_id]
        
    return {"message": "Idea deleted successfully"}

@router.post("/{idea_id}/review")
def admin_review_idea(idea_id: str, data: IdeaReview, admin_user_id: str = "admin"):
    """
    Admin reviews an idea:
    - Updates status (reviewed, selected, rejected)
    - Adds admin comment
    - Optionally assigns mentor
    - Updates student's RISE score if selected
    """
    idea = ideas_db.get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    if data.status not in ["reviewed", "selected", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    # Update idea
    idea["status"] = data.status
    idea["reviewed_at"] = datetime.utcnow().isoformat()
    
    if data.mentor_assignment and data.mentor_assignment in mentors_db:
        idea["mentor_suggestions"] = [data.mentor_assignment]  # Replace with assigned mentor
    
    # Add admin comment
    if data.admin_comment:
        comment = {
            "admin_id": admin_user_id,
            "comment": data.admin_comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        if idea_id not in idea_comments_db:
            idea_comments_db[idea_id] = []
        idea_comments_db[idea_id].append(comment)
    
    # Update RISE score if selected
    rise_boost = 0
    if data.status == "selected":
        rise_boost = adjust_rise_score_for_idea(idea["student_id"], "selected")
        idea["rise_score_impact"] = rise_boost
    elif data.status == "reviewed":
        rise_boost = adjust_rise_score_for_idea(idea["student_id"], "reviewed")
        idea["rise_score_impact"] = rise_boost
    
    return {
        "success": True,
        "idea_id": idea_id,
        "status": idea["status"],
        "rise_score_boost": rise_boost,
        "message": f"Idea marked as {data.status}. Student RISE score updated: +{rise_boost} points"
    }

@router.post("/{idea_id}/comment")
def add_admin_comment(idea_id: str, data: CommentAdd, admin_user_id: str = "admin"):
    """
    Admin adds a comment to an idea (without changing status)
    """
    idea = ideas_db.get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    if not data.comment or len(data.comment.strip()) < 3:
        raise HTTPException(status_code=400, detail="Comment must be at least 3 characters")
    
    comment = {
        "admin_id": admin_user_id,
        "comment": data.comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    if idea_id not in idea_comments_db:
        idea_comments_db[idea_id] = []
    idea_comments_db[idea_id].append(comment)
    
    return {
        "success": True,
        "idea_id": idea_id,
        "comment_added": comment
    }

@router.get("/admin/stats")
def admin_ideas_stats():
    """
    Admin dashboard: Stats on idea submissions
    """
    total = len(ideas_db)
    by_status = {}
    by_category = {}
    
    for idea in ideas_db.values():
        # Count by status
        status = idea["status"]
        by_status[status] = by_status.get(status, 0) + 1
        
        # Count by category
        cat = idea["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    
    total_rise_boost = sum(idea.get("rise_score_impact", 0) for idea in ideas_db.values())
    
    return {
        "total_ideas": total,
        "by_status": by_status,
        "by_category": by_category,
        "total_rise_score_distributed": total_rise_boost,
        "avg_feasibility": round(sum(idea.get("feasibility_score", 0) for idea in ideas_db.values()) / max(total, 1), 2)
    }

@router.get("/admin/export-csv")
def admin_export_ideas_csv():
    """
    Export all ideas as CSV for reporting
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "ID", "Student", "Title", "Category", "Feasibility", "Status", 
        "Submitted", "Reviewed", "RISE Impact", "Mentors"
    ])
    
    writer.writeheader()
    for idea in ideas_db.values():
        writer.writerow({
            "ID": idea["id"][:8],
            "Student": idea["student_id"],
            "Title": idea["title"],
            "Category": idea["category"],
            "Feasibility": idea["feasibility_score"],
            "Status": idea["status"],
            "Submitted": idea["submitted_at"][:10],
            "Reviewed": idea.get("reviewed_at", "N/A")[:10] if idea.get("reviewed_at") else "N/A",
            "RISE Impact": idea.get("rise_score_impact", 0),
            "Mentors": ", ".join(idea.get("mentor_suggestions", []))
        })
    
    return {
        "csv_data": output.getvalue(),
        "filename": f"ideas_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    }
