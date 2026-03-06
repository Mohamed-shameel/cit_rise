"""
RISE Score adjustments based on opportunity participation
"""
import json
from datetime import datetime

# Score impact mappings
OPPORTUNITY_SCORE_IMPACT = {
    "internship": {
        "completed": 30,
        "dropped": -10,
        "registered": 5
    },
    "competition": {
        "completed": 40,  # Higher value for winning/completion
        "dropped": -15,
        "registered": 8
    },
    "research": {
        "completed": 50,  # Research is highly valued
        "dropped": -20,
        "registered": 5
    },
    "job": {
        "completed": 25,  # Job offer/acceptance
        "dropped": -10,
        "registered": 3
    },
    "workshop": {
        "completed": 15,
        "dropped": -5,
        "registered": 2
    },
    "fellowship": {
        "completed": 45,
        "dropped": -15,
        "registered": 8
    },
    "opportunity": {
        "completed": 20,
        "dropped": -8,
        "registered": 3
    }
}

def calculate_opportunity_impact(opportunity_type: str, status: str) -> int:
    """
    Calculate RISE score impact based on opportunity type and status
    
    Args:
        opportunity_type: Type of opportunity (internship, competition, etc)
        status: Current status (registered, ongoing, completed, dropped)
    
    Returns:
        Points to add/subtract from RISE score
    """
    type_lower = opportunity_type.lower() if opportunity_type else "opportunity"
    status_lower = status.lower() if status else "registered"
    
    impact_map = OPPORTUNITY_SCORE_IMPACT.get(type_lower, OPPORTUNITY_SCORE_IMPACT["opportunity"])
    return impact_map.get(status_lower, 0)

def update_rise_score_for_opportunity(user: dict, user_opportunities_list: list, opportunities_db: dict) -> dict:
    """
    Recalculate RISE score based on all user's opportunity participation
    
    Args:
        user: User dictionary
        user_opportunities_list: List of user's opportunity registrations
        opportunities_db: Database of opportunities
    
    Returns:
        Updated user with new RISE score
    """
    opportunity_boost = 0
    opportunity_details = {
        "completed_count": 0,
        "dropped_count": 0,
        "registered_count": 0,
        "breakdown": {}
    }
    
    for uo in user_opportunities_list:
        opp_id = uo.get("opportunity_id")
        status = uo.get("status", "registered")
        
        # Get opportunity details
        opp = opportunities_db.get(opp_id, {})
        opp_type = opp.get("type", "opportunity")
        
        # Calculate impact
        impact = calculate_opportunity_impact(opp_type, status)
        opportunity_boost += impact
        
        # Track details
        if status == "completed":
            opportunity_details["completed_count"] += 1
        elif status == "dropped":
            opportunity_details["dropped_count"] += 1
        elif status == "registered":
            opportunity_details["registered_count"] += 1
        
        # Store breakdown
        key = f"{opp_type}_{status}"
        opportunity_details["breakdown"][key] = opportunity_details["breakdown"].get(key, 0) + impact
    
    # Store opportunity contribution
    user["opportunity_contribution"] = {
        "total_boost": opportunity_boost,
        "details": opportunity_details,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    return user, opportunity_boost

def generate_opportunity_insights(user_opportunities_list: list, opportunities_db: dict) -> str:
    """
    Generate AI-friendly insights about user's opportunity participation
    for use in RISE score reasoning
    """
    if not user_opportunities_list:
        return "No opportunity participation yet."
    
    completed = [uo for uo in user_opportunities_list if uo.get("status") == "completed"]
    ongoing = [uo for uo in user_opportunities_list if uo.get("status") == "ongoing"]
    registered = [uo for uo in user_opportunities_list if uo.get("status") == "registered"]
    dropped = [uo for uo in user_opportunities_list if uo.get("status") == "dropped"]
    
    insights = []
    
    if completed:
        completed_types = [opportunities_db.get(uo.get("opportunity_id"), {}).get("type", "opportunity") 
                          for uo in completed]
        insights.append(f"Completed {len(completed)} opportunities: {', '.join(set(completed_types))}")
    
    if ongoing:
        insights.append(f"Currently pursuing {len(ongoing)} opportunities")
    
    if registered:
        insights.append(f"Registered for {len(registered)} additional opportunities")
    
    if dropped:
        insights.append(f"⚠️ Dropped {len(dropped)} opportunities (commitment concern)")
    
    return " | ".join(insights) if insights else "Limited opportunity engagement"


# ============== IDEAS SCORING ==============

IDEA_SCORE_IMPACT = {
    "reviewed": 20,      # Idea reviewed by admin
    "selected": 40,      # Idea selected/approved for implementation
    "rejected": 0        # No score change
}

def adjust_rise_score_for_idea(user_id: str, status: str) -> int:
    """
    Adjust RISE score based on idea review status
    Called when admin reviews/selects an idea
    
    Args:
        user_id: Student who submitted the idea
        status: Review status (reviewed, selected, rejected)
    
    Returns:
        Points added to RISE score
    """
    from config.store import users_db
    
    if user_id not in users_db:
        return 0
    
    points = IDEA_SCORE_IMPACT.get(status, 0)
    
    if points > 0:
        users_db[user_id]["rise_score"] = users_db[user_id].get("rise_score", 0) + points
    
    return points


def generate_idea_insights(user_ideas: list) -> str:
    """
    Generate insights about user's idea submissions for RISE score reasoning
    """
    if not user_ideas:
        return "No ideas submitted yet."
    
    selected = [idea for idea in user_ideas if idea.get("status") == "selected"]
    reviewed = [idea for idea in user_ideas if idea.get("status") == "reviewed"]
    pending = [idea for idea in user_ideas if idea.get("status") == "pending"]
    
    insights = []
    
    if selected:
        insights.append(f"✨ {len(selected)} selected innovation(s)")
    
    if reviewed:
        insights.append(f"📋 {len(reviewed)} idea(s) under review")
    
    if pending:
        insights.append(f"📝 {len(pending)} idea(s) pending admin review")
    
    return " | ".join(insights) if insights else "Innovation ideas pending review"

