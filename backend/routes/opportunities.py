from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from config.store import opportunities_db, user_opportunities, deduplication_log, scraper_logs, users_db
from services.scraper_service import (
    scrape_unstop_html, scrape_hackerrank_mock, scrape_internshala_mock,
    enrich_opportunity_with_ai, find_duplicates, merge_opportunities
)
from services.opportunity_scoring import calculate_opportunity_impact

router = APIRouter()

# ─────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────

class OppCreate(BaseModel):
    title: str
    description: str
    domain: List[str]
    type: str = "opportunity"
    company: str
    location: Optional[str] = "India"
    source_url: str
    deadline: Optional[str] = None
    salary_range: Optional[str] = None
    duration: Optional[str] = None

class OppUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[List[str]] = None
    type: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    source_url: Optional[str] = None
    deadline: Optional[str] = None
    salary_range: Optional[str] = None
    duration: Optional[str] = None

class UserOppRegister(BaseModel):
    user_id: str

class UserOppStatusUpdate(BaseModel):
    status: str  # registered|ongoing|completed|dropped

# ─────────────────────────────────────────────────
# Student Endpoints
# ─────────────────────────────────────────────────

@router.get("/")
async def list_opps(
    type: Optional[str] = None,
    department: Optional[str] = None,
    sort_by: str = "deadline"
):
    """List all opportunities with optional filters"""
    opps = list(opportunities_db.values())
    
    # Filter by type
    if type:
        opps = [o for o in opps if o.get("type") == type]
    
    # Filter by department fit
    if department:
        opps = [o for o in opps if department in o.get("department_fit", [])]
    
    # Sort
    if sort_by == "deadline":
        opps = sorted(opps, key=lambda x: x.get("deadline", "9999-12-31"), reverse=False)
    elif sort_by == "recently_added":
        opps = sorted(opps, key=lambda x: x.get("created_at", ""), reverse=True)
    elif sort_by == "relevance":
        opps = sorted(opps, key=lambda x: x.get("ai_analysis", {}).get("relevance_score", 5), reverse=True)
    
    return {"total": len(opps), "opportunities": opps}

@router.get("/matched/{student_id}")
async def get_matched_opportunities(student_id: str):
    """Return opportunities sorted by AI match score for a student"""
    student = users_db.get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    dept = student.get("department", "")
    skills = set(s.lower() for s in student.get("skills", []))
    interests = set(i.lower() for i in student.get("interests", []))

    matched = []
    for opp in opportunities_db.values():
        score = 0
        reasons = []

        domains = opp.get("domain", [])
        if isinstance(domains, str):
            domains = [domains]
        domains_lower = set(d.lower() for d in domains)

        if dept in opp.get("department_fit", []):
            score += 35
            reasons.append("Matches your department")

        if domains_lower & interests:
            score += 25
            reasons.append("Aligns with your interests")

        for skill in skills:
            if any(skill in d or d in skill for d in domains_lower):
                score += 20
                reasons.append("Skill alignment detected")
                break

        ai_score = opp.get("ai_analysis", {}).get("relevance_score", 5)
        score += int(ai_score * 2)

        matched.append({
            **opp,
            "match_score": min(score, 100),
            "match_reasons": reasons[:2] if reasons else ["General opportunity"],
        })

    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return {"student_id": student_id, "total": len(matched), "opportunities": matched}


@router.get("/user/{user_id}")
async def get_user_opportunities(user_id: str):
    """Get opportunities a user has registered for"""
    user_opps = [uo for uo in user_opportunities.values() if uo.get("user_id") == user_id]
    
    result = []
    for uo in user_opps:
        opp_id = uo.get("opportunity_id")
        opp = opportunities_db.get(opp_id)
        if opp:
            result.append({
                "registration": uo,
                "opportunity": opp
            })
    
    return {"total": len(result), "opportunities": result}

@router.post("/{opp_id}/register")
async def register_for_opportunity(opp_id: str, user_opp: UserOppRegister):
    """User registers for an opportunity"""
    if opp_id not in opportunities_db:
        raise HTTPException(404, "Opportunity not found")
    
    # Check if already registered
    existing = [uo for uo in user_opportunities.values() 
                if uo.get("user_id") == user_opp.user_id and uo.get("opportunity_id") == opp_id]
    
    if existing:
        raise HTTPException(400, "Already registered for this opportunity")
    
    uo_id = f"uo_{uuid.uuid4().hex[:8]}"
    user_opportunities[uo_id] = {
        "user_opp_id": uo_id,
        "user_id": user_opp.user_id,
        "opportunity_id": opp_id,
        "status": "registered",
        "registered_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "completed_at": None
    }
    
    # Apply registration bonus to RISE score
    opp = opportunities_db[opp_id]
    opp_type = opp.get("type", "opportunity")
    bonus = calculate_opportunity_impact(opp_type, "registered")
    
    user = users_db.get(user_opp.user_id)
    if user:
        user["rise_score"] = user.get("rise_score", 0) + bonus
    
    return {"message": "Registered successfully", "user_opp_id": uo_id, "rise_score_bonus": bonus}

@router.put("/{opp_id}/user/{user_id}/status")
async def update_opportunity_status(opp_id: str, user_id: str, update: UserOppStatusUpdate):
    """Update user's opportunity status (ongoing/completed/dropped)"""
    uo = None
    uo_id = None
    
    for uid, uo_record in user_opportunities.items():
        if uo_record.get("user_id") == user_id and uo_record.get("opportunity_id") == opp_id:
            uo = uo_record
            uo_id = uid
            break
    
    if not uo:
        raise HTTPException(404, "Registration not found")
    
    old_status = uo.get("status", "registered")
    uo["status"] = update.status
    uo["updated_at"] = datetime.utcnow().isoformat()
    
    if update.status == "completed":
        uo["completed_at"] = datetime.utcnow().isoformat()
    elif update.status == "ongoing":
        uo["started_at"] = datetime.utcnow().isoformat()
    
    # Calculate RISE score impact
    opp = opportunities_db.get(opp_id, {})
    opp_type = opp.get("type", "opportunity")
    
    old_impact = calculate_opportunity_impact(opp_type, old_status)
    new_impact = calculate_opportunity_impact(opp_type, update.status)
    score_delta = new_impact - old_impact
    
    # Update user's RISE score
    user = users_db.get(user_id)
    if user:
        user["rise_score"] = user.get("rise_score", 0) + score_delta
    
    return {
        "message": "Status updated",
        "registration": uo,
        "score_impact": score_delta,
        "new_rise_score": user.get("rise_score", 0) if user else None
    }

# ─────────────────────────────────────────────────
# Admin Endpoints
# ─────────────────────────────────────────────────

@router.post("/admin/create")
async def admin_create_opportunity(opp: OppCreate):
    """Admin creates a custom opportunity"""
    
    # Check for duplicates
    new_opp_dict = opp.model_dump()
    new_opp_dict["source"] = "admin"
    new_opp_dict["verified"] = False
    
    duplicate_id = find_duplicates(new_opp_dict, opportunities_db)
    if duplicate_id:
        raise HTTPException(400, f"Similar opportunity already exists: {duplicate_id}")
    
    # Create opportunity
    opp_id = f"opp_{uuid.uuid4().hex[:8]}"
    opp_record = {
        "opportunity_id": opp_id,
        **opp.model_dump(),
        "source": "admin",
        "source_id": f"admin_{opp_id}",
        "source_url": opp.source_url,
        "verified": False,
        "department_fit": [],
        "ai_analysis": {},
        "posted_date": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    # Enrich with AI
    opp_record = await enrich_opportunity_with_ai(opp_record)
    
    opportunities_db[opp_id] = opp_record
    
    return {"message": "Opportunity created", "opportunity_id": opp_id, "opportunity": opp_record}

@router.put("/admin/{opp_id}")
async def admin_update_opportunity(opp_id: str, update: OppUpdate):
    """Admin updates an opportunity"""
    if opp_id not in opportunities_db:
        raise HTTPException(404, "Opportunity not found")
    
    opp = opportunities_db[opp_id]
    for k, v in update.model_dump(exclude_none=True).items():
        opp[k] = v
    opp["updated_at"] = datetime.utcnow().isoformat()
    return {"message": "Opportunity updated", "opportunity": opp}

@router.put("/admin/{opp_id}/verify")
async def admin_verify_opportunity(opp_id: str):
    """Admin verifies a custom opportunity"""
    if opp_id not in opportunities_db:
        raise HTTPException(404, "Opportunity not found")
    
    opp = opportunities_db[opp_id]
    opp["verified"] = True
    opp["updated_at"] = datetime.utcnow().isoformat()
    
    return {"message": "Opportunity verified", "opportunity": opp}

@router.post("/admin/sync-unstop")
async def admin_sync_unstop():
    """Admin triggers Unstop scraper"""
    try:
        new_opps = await scrape_unstop_html()
        
        added = 0
        duplicates = 0
        
        for new_opp in new_opps:
            # Check for duplicates
            duplicate_id = find_duplicates(new_opp, opportunities_db)
            
            if duplicate_id:
                # Log the duplicate
                merge_record = merge_opportunities(duplicate_id, new_opp.get("source_id"), "unstop")
                deduplication_log[merge_record["merge_id"]] = merge_record
                duplicates += 1
            else:
                # Add new opportunity
                opp_id = new_opp.get("opportunity_id", f"opp_{uuid.uuid4().hex[:8]}")
                
                # Enrich with AI
                new_opp = await enrich_opportunity_with_ai(new_opp)
                
                opportunities_db[opp_id] = new_opp
                added += 1
        
        # Log the sync operation
        sync_log_id = f"sync_{uuid.uuid4().hex[:8]}"
        scraper_logs[sync_log_id] = {
            "sync_id": sync_log_id,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "unstop",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "status": "completed"
        }
        
        return {
            "message": "Sync completed",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "total_opportunities": len(opportunities_db)
        }
    
    except Exception as e:
        raise HTTPException(500, f"Sync failed: {str(e)}")

@router.post("/admin/sync-hackerrank")
async def admin_sync_hackerrank():
    """Admin triggers HackerRank scraper"""
    try:
        new_opps = await scrape_hackerrank_mock()
        added = 0
        duplicates = 0
        for new_opp in new_opps:
            duplicate_id = find_duplicates(new_opp, opportunities_db)
            if duplicate_id:
                merge_record = merge_opportunities(duplicate_id, new_opp.get("source_id"), "hackerrank")
                deduplication_log[merge_record["merge_id"]] = merge_record
                duplicates += 1
            else:
                opp_id = new_opp.get("opportunity_id", f"opp_{uuid.uuid4().hex[:8]}")
                new_opp = await enrich_opportunity_with_ai(new_opp)
                opportunities_db[opp_id] = new_opp
                added += 1
        
        sync_log_id = f"sync_{uuid.uuid4().hex[:8]}"
        scraper_logs[sync_log_id] = {
            "sync_id": sync_log_id,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "hackerrank",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "status": "completed"
        }
        return {
            "message": "Sync completed",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "total_opportunities": len(opportunities_db)
        }
    except Exception as e:
        raise HTTPException(500, f"Sync failed: {str(e)}")

@router.post("/admin/sync-internshala")
async def admin_sync_internshala():
    """Admin triggers Internshala scraper"""
    try:
        new_opps = await scrape_internshala_mock()
        added = 0
        duplicates = 0
        for new_opp in new_opps:
            duplicate_id = find_duplicates(new_opp, opportunities_db)
            if duplicate_id:
                merge_record = merge_opportunities(duplicate_id, new_opp.get("source_id"), "internshala")
                deduplication_log[merge_record["merge_id"]] = merge_record
                duplicates += 1
            else:
                opp_id = new_opp.get("opportunity_id", f"opp_{uuid.uuid4().hex[:8]}")
                new_opp = await enrich_opportunity_with_ai(new_opp)
                opportunities_db[opp_id] = new_opp
                added += 1
        
        sync_log_id = f"sync_{uuid.uuid4().hex[:8]}"
        scraper_logs[sync_log_id] = {
            "sync_id": sync_log_id,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "internshala",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "status": "completed"
        }
        return {
            "message": "Sync completed",
            "total_fetched": len(new_opps),
            "added": added,
            "duplicates": duplicates,
            "total_opportunities": len(opportunities_db)
        }
    except Exception as e:
        raise HTTPException(500, f"Sync failed: {str(e)}")

@router.get("/admin/sync-logs")
async def get_sync_logs():
    """Get history of scraper operations"""
    logs = sorted(scraper_logs.values(), key=lambda x: x.get("timestamp", ""), reverse=True)
    return {"total": len(logs), "logs": logs}

@router.get("/admin/deduplication-logs")
async def get_deduplication_logs():
    """Get history of merged opportunities"""
    logs = sorted(deduplication_log.values(), key=lambda x: x.get("merged_at", ""), reverse=True)
    return {"total": len(logs), "logs": logs}

@router.delete("/admin/{opp_id}")
async def admin_delete_opportunity(opp_id: str):
    """Admin deletes an opportunity"""
    if opp_id not in opportunities_db:
        raise HTTPException(404, "Opportunity not found")
    
    del opportunities_db[opp_id]
    return {"message": "Opportunity deleted"}

@router.get("/admin/all")
async def admin_list_all_opportunities():
    """Admin view: list all opportunities with metadata"""
    opps = list(opportunities_db.values())
    
    verified = [o for o in opps if o.get("verified", False)]
    unverified = [o for o in opps if not o.get("verified", False)]
    
    return {
        "total": len(opps),
        "verified_count": len(verified),
        "unverified_count": len(unverified),
        "opportunities": opps
    }

