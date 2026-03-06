"""
Ideas Submission System Routes
Allows students to submit innovation ideas, get AI analysis, and admins to review
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import qrcode
from io import BytesIO
import base64

from config.store import ideas_db, idea_comments_db, idea_submissions_log, mentors_db, users_db
from services.ai_service import analyze_idea
from services.opportunity_scoring import adjust_rise_score_for_idea

router = APIRouter()

# Pydantic models
class IdeaSubmit(BaseModel):
    title: str
    description: str
    optional_files: str = None  # For future file upload

class IdeaReview(BaseModel):
    status: str  # 'reviewed', 'selected', 'rejected'
    admin_comment: str = ""
    mentor_assignment: str = None

class CommentAdd(BaseModel):
    comment: str

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

# Helper: Generate QR code
def generate_qr_code(idea_id: str) -> str:
    """Generate QR code that links to idea submission form"""
    qr_url = f"http://localhost:3000/submit-idea?idea_id={idea_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure directory exists
    os.makedirs("qr_codes", exist_ok=True)
    filepath = f"qr_codes/{idea_id}.png"
    img.save(filepath)
    
    return f"/qr/{idea_id}.png"

# Helper: Generate idea ID
def gen_idea_id():
    return str(uuid.uuid4())

# ============== STUDENT ENDPOINTS ==============

@router.post("/submit")
async def submit_idea(data: IdeaSubmit, user_id: str = "student_demo"):
    """
    Student submits a new innovation idea
    - Title and description required
    - AI analysis triggered automatically
    - QR code generated for sharing
    - Returns: idea_id, qr_url, ai_analysis
    """
    if not data.title or len(data.title.strip()) < 5:
        raise HTTPException(status_code=400, detail="Title must be at least 5 characters")
    if not data.description or len(data.description.strip()) < 20:
        raise HTTPException(status_code=400, detail="Description must be at least 20 characters")
    
    idea_id = gen_idea_id()
    
    try:
        # Get AI analysis (category, feasibility, mentor suggestions)
        ai_analysis = await analyze_idea(data.title, data.description)
    except Exception as e:
        ai_analysis = {
            "category": "General Innovation",
            "feasibility_score": 50,
            "mentor_suggestions": list(mentors_db.keys())[:2] if mentors_db else [],
            "error": str(e)
        }
    
    # Generate QR code
    qr_url = generate_qr_code(idea_id)
    
    # Create idea record
    idea = {
        "id": idea_id,
        "student_id": user_id,
        "title": data.title,
        "description": data.description,
        "category": ai_analysis.get("category", "General Innovation"),
        "feasibility_score": ai_analysis.get("feasibility_score", 50),
        "mentor_suggestions": ai_analysis.get("mentor_suggestions", []),
        "status": "pending",  # pending, reviewed, selected, rejected
        "submitted_at": datetime.utcnow().isoformat(),
        "reviewed_at": None,
        "qr_code_url": qr_url,
        "rise_score_impact": 0
    }
    
    # Store in database
    ideas_db[idea_id] = idea
    idea_comments_db[idea_id] = []
    
    # Update analytics
    idea_submissions_log["total"] = len(ideas_db)
    cat = idea["category"]
    idea_submissions_log["categories"][cat] = idea_submissions_log["categories"].get(cat, 0) + 1
    
    return {
        "success": True,
        "idea_id": idea_id,
        "qr_url": qr_url,
        "ai_analysis": ai_analysis,
        "message": "Idea submitted successfully! Share QR code with peers or admin."
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
