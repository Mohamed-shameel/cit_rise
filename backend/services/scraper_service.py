import httpx
import json
from datetime import datetime
import uuid
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scrape_unstop() -> List[Dict]:
    """Scrape opportunities from Unstop.com"""
    opportunities = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch main opportunities page
            url = "https://unstop.com/api/v1/opportunities"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            # Note: This is a simplified example. Unstop may require specific headers/params
            # In reality, we'd use BeautifulSoup to parse the HTML or find their actual API
            response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                logger.warning(f"Unstop scrape failed: {response.status_code}")
                # For now, return empty list - in production, try fallback URLs
                return opportunities
            
            data = response.json()
            
            # Parse opportunities based on Unstop's response structure
            for item in data.get("data", []):
                try:
                    opp_type = classify_opportunity_type(item.get("category", ""))
                    
                    opp = {
                        "opportunity_id": f"unstop_{item.get('id', uuid.uuid4().hex[:8])}",
                        "title": item.get("title", ""),
                        "description": item.get("description", "")[:500],  # Truncate
                        "domain": extract_domains(item.get("category", "")),
                        "type": opp_type,
                        "company": item.get("organization_name", "Unstop"),
                        "location": item.get("location", "India"),
                        "source": "unstop",
                        "source_id": f"unstop_{item.get('id')}",
                        "source_url": item.get("url", "https://unstop.com"),
                        "posted_date": item.get("published_at", datetime.utcnow().isoformat()),
                        "deadline": item.get("deadline", ""),
                        "verified": True,
                        "ai_analysis": {},  # Will be filled by AI service later
                        "created_at": datetime.utcnow().isoformat(),
                        "updated_at": datetime.utcnow().isoformat(),
                    }
                    opportunities.append(opp)
                except Exception as e:
                    logger.error(f"Error parsing Unstop item: {e}")
                    continue
        
        logger.info(f"Scraped {len(opportunities)} opportunities from Unstop")
        
    except Exception as e:
        logger.error(f"Unstop scraper error: {e}")
    
    return opportunities


async def scrape_unstop_html() -> List[Dict]:
    """
    Fetch opportunities directly from Unstop's public API
    (Replaces the broken beautifulsoup HTML scraper)
    """
    opportunities = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = "https://unstop.com/api/public/opportunity/search-result?opportunity=competitions"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.warning(f"Unstop API scrape failed: {response.status_code}")
                return opportunities
                
            data = response.json()
            items = data.get("data", {}).get("data", [])
            
            for item in items:
                try:
                    title_text = item.get("title", "Untitled")
                    seo_url = item.get("seo_url", "")
                    card_link = f"https://unstop.com/competitions/{seo_url}" if seo_url else "https://unstop.com"
                    
                    org = item.get("organisation", {})
                    company_text = org.get("name") if isinstance(org, dict) else "Unstop"
                    
                    deadline_text = item.get("end_date", "")
                    
                    tags = item.get("tags", [])
                    category_text = ", ".join([t.get("name", "") for t in tags if isinstance(t, dict)]) if tags else ""
                    type_str = item.get("type", "competition")
                    
                    opp = {
                        "opportunity_id": f"unstop_{uuid.uuid4().hex[:8]}",
                        "title": title_text,
                        "description": item.get("details", "Click to view full details on Unstop.")[:500],
                        "domain": extract_domains(category_text + " " + title_text),
                        "type": classify_opportunity_type(type_str + " " + category_text),
                        "company": company_text,
                        "location": "Online / India",
                        "source": "unstop",
                        "source_id": f"unstop_{item.get('id')}",
                        "source_url": card_link,
                        "deadline": deadline_text,
                        "verified": True,
                        "created_at": datetime.utcnow().isoformat(),
                        "updated_at": datetime.utcnow().isoformat(),
                    }
                    opportunities.append(opp)
                except Exception as e:
                    logger.error(f"Error parsing item: {e}")
                    continue
        
        logger.info(f"Scraped {len(opportunities)} opportunities from Unstop API")
        
    except Exception as e:
        logger.error(f"Unstop API scraper error: {e}")
    
    return opportunities


def classify_opportunity_type(category: str) -> str:
    """Map Unstop category to our opportunity types"""
    category_lower = category.lower()
    
    if any(word in category_lower for word in ["hackathon", "hack", "coding contest"]):
        return "competition"
    elif any(word in category_lower for word in ["research", "paper", "publication"]):
        return "research"
    elif any(word in category_lower for word in ["internship", "intern"]):
        return "internship"
    elif any(word in category_lower for word in ["job", "position", "opening"]):
        return "job"
    elif any(word in category_lower for word in ["workshop", "webinar", "seminar"]):
        return "workshop"
    elif any(word in category_lower for word in ["fellowship", "grant"]):
        return "fellowship"
    else:
        return "opportunity"


def extract_domains(category: str) -> List[str]:
    """Extract relevant domains/tags from category"""
    domains = []
    category_lower = category.lower()
    
    domain_keywords = {
        "AI/ML": ["ai", "ml", "machine learning", "artificial intelligence", "deep learning", "nlp"],
        "Web Development": ["web", "frontend", "backend", "full stack", "react", "node"],
        "Data Science": ["data science", "data", "analytics", "big data"],
        "Cybersecurity": ["security", "cyber", "penetration", "hacking"],
        "Cloud": ["cloud", "aws", "azure", "gcp", "kubernetes"],
        "Robotics": ["robotics", "robot", "embedded", "iot"],
        "Mobile": ["mobile", "android", "ios", "flutter"],
        "DevOps": ["devops", "ci/cd", "docker", "devops"],
        "Blockchain": ["blockchain", "crypto", "web3"],
        "Startup": ["startup", "entrepreneurship", "venture", "pitch"],
        "IoT": ["iot", "embedded", "hardware"],
    }
    
    for domain, keywords in domain_keywords.items():
        if any(keyword in category_lower for keyword in keywords):
            domains.append(domain)
    
    if not domains:
        domains.append("Opportunity")
    
    return list(set(domains))  # Remove duplicates


async def enrich_opportunity_with_ai(opportunity: Dict) -> Dict:
    """
    Use Gemini to analyze and enrich opportunity data
    - Infer department fit
    - Calculate relevance score
    - Generate summary
    """
    from services.ai_service import call_gemini
    import json
    
    try:
        prompt = f"""Analyze this opportunity and provide structured analysis:

Title: {opportunity.get('title', '')}
Company: {opportunity.get('company', '')}
Type: {opportunity.get('type', '')}
Domain: {', '.join(opportunity.get('domain', []))}
Description: {opportunity.get('description', '')[:300]}

Return JSON with:
- department_fit: array of departments (CSE, CSE AI, IT, ECE, MECH, EEE) that match
- relevance_score: 1-10 score for a typical student
- difficulty_level: Easy/Medium/Hard
- learning_value: Low/Medium/High
- category_confidence: 0-1 confidence in categorization
- brief_summary: 1 sentence summary

Only return valid JSON, no markdown."""
        
        response = await call_gemini(prompt, "You are an opportunity analyst for a college platform.")
        
        try:
            analysis = json.loads(response)
        except:
            # If AI returns invalid JSON, provide defaults
            analysis = {
                "department_fit": ["CSE", "IT"],
                "relevance_score": 6,
                "difficulty_level": "Medium",
                "learning_value": "Medium",
                "category_confidence": 0.7,
                "brief_summary": opportunity.get('title', 'Opportunity')
            }
        
        opportunity["ai_analysis"] = analysis
        opportunity["department_fit"] = analysis.get("department_fit", [])
        
    except Exception as e:
        logger.error(f"AI enrichment error: {e}")
        opportunity["ai_analysis"] = {}
        opportunity["department_fit"] = ["CSE", "IT"]  # Default fallback
    
    return opportunity


def find_duplicates(new_opp: Dict, existing_opps: Dict) -> str:
    """
    Find if new_opp is a duplicate of an existing one
    Returns the opp_id of the matched opportunity, or None if no match
    """
    new_title = new_opp.get("title", "").lower().strip()
    new_deadline = new_opp.get("deadline", "").strip()
    new_company = new_opp.get("company", "").lower().strip()
    new_url = new_opp.get("source_url", "").lower().strip()
    
    for opp_id, existing in existing_opps.items():
        existing_title = existing.get("title", "").lower().strip()
        existing_deadline = existing.get("deadline", "").strip()
        existing_company = existing.get("company", "").lower().strip()
        existing_url = existing.get("source_url", "").lower().strip()
        
        # Exact match on URL
        if new_url and existing_url and new_url == existing_url:
            return opp_id
        
        # Match on title + company + deadline (fuzzy)
        if (new_title == existing_title and 
            new_company == existing_company and 
            new_deadline == existing_deadline):
            return opp_id
        
        # Partial match: similar title and same deadline
        if (similar_strings(new_title, existing_title, 0.85) and 
            new_deadline == existing_deadline):
            return opp_id
    
    return None


def similar_strings(s1: str, s2: str, threshold: float = 0.8) -> bool:
    """Check if two strings are similar (Levenshtein-like check)"""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, s1, s2).ratio() >= threshold


def merge_opportunities(primary_opp_id: str, duplicate_opp_id: str, duplicate_source: str) -> Dict:
    """
    Record a deduplication merge
    Returns record for dedup_log
    """
    return {
        "merge_id": f"dedup_{uuid.uuid4().hex[:8]}",
        "primary_opp_id": primary_opp_id,
        "duplicate_opp_id": duplicate_opp_id,
        "duplicate_source": duplicate_source,
        "merged_at": datetime.utcnow().isoformat(),
        "reason": "Duplicate opportunity detected"
    }
