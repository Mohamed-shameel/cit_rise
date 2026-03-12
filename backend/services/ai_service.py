import os, json
import httpx
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3-8b-instruct"
GITHUB_API_BASE = "https://api.github.com"


async def call_llama(prompt: str, system: str = "") -> str:
    if not API_KEY:
        return '{"error":"no_key"}'
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.post(URL, json=payload, headers=headers)
        d = r.json()
        
    try:
        return d["choices"][0]["message"]["content"]
    except Exception:
        return json.dumps({"error": str(d.get("error", "unknown"))})


def parse(raw: str, fallback: dict) -> dict:
    try:
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return fallback


async def generate_student_profile(resume_text: str, github: Optional[str] = None) -> dict:
    sys = "Extract a structured student profile from a resume for CIT RISE platform. JSON only, no markdown."
    gh = f"\nGitHub: {github}" if github else ""
    prompt = f"""Extract profile from resume below.{gh}

Resume:
{resume_text[:3000]}

Return JSON:
{{"name":"string","department":"CSE/ECE/MECH/IT/EEE/CSE AI","year":2,"skills":["list"],"interests":["list"],
"strengths":["3 phrases"],"profile_summary":"2-3 sentences","innovation_potential":"High/Medium/Low",
"suggested_roles":["3 roles"],"resume_suggestions":["specific improvement tip 1","specific improvement tip 2","specific improvement tip 3"]}}"""
    raw = await call_llama(prompt, sys)
    return parse(raw, {"name":"Student","department":"CSE","year":2,"skills":["Python"],"interests":["Technology"],
        "strengths":["Analytical","Fast learner","Team player"],"profile_summary":"Motivated student with good technical skills.",
        "innovation_potential":"Medium","suggested_roles":["Software Engineer","ML Engineer","Web Developer"],
        "innovation_potential":"Medium","suggested_roles":["Software Engineer","ML Engineer","Web Developer"],
        "resume_suggestions":["Add measurable impact metrics to each achievement","Include links to GitHub projects or live demos","Add a clear technical skills section with proficiency levels"]})


async def regenerate_student_profile(student: dict) -> dict:
    sys = "Regenerate AI profile summary for CIT RISE student based on their current profile. JSON only, no markdown."
    prompt = f"""Regenerate the profile summary and suggested learning roles for this student based on their data.

Student: {student.get('name')} | {student.get('department')} | Year {student.get('year')}
Skills: {', '.join(student.get('skills', []))}
Interests: {', '.join(student.get('interests', []))}
Achievements: {', '.join([a.get('title', '') for a in student.get('achievements', [])]) if student.get('achievements') else 'None'}

Return JSON:
{{"profile_summary":"2-3 sentences summarizing their potential and skills","suggested_roles":["3 roles"]}}"""
    raw = await call_llama(prompt, sys)
    return parse(raw, {
        "profile_summary":"Driven student actively building technical skills.",
        "suggested_roles":["Software Engineer", "Developer"]
    })


async def calculate_rise_score(student: dict, achievements: list) -> dict:
    sys = "You are CIT RISE Score AI. Evaluate students holistically. JSON only."
    ach = "\n".join([f"- {a['title']} ({a['type']})" for a in achievements]) or "No achievements yet."
    prompt = f"""Score this student 0-500 on CIT RISE Innovation Scale.

{student.get('name')} | {student.get('department')} | Year {student.get('year')}
Skills: {', '.join(student.get('skills',[]))}
Achievements:\n{ach}

JSON:
{{"total_score":200,"breakdown":{{"achievement_quality":80,"skill_depth":60,"research_impact":30,"innovation_mindset":20,"leadership_potential":10}},
"percentile":"top X%","score_reasoning":"2-3 sentences","improvement_areas":["2 things"],"badge":"Pioneer/Innovator/Explorer/Starter"}}"""
    raw = await call_llama(prompt, sys)
    return parse(raw, {"total_score":180,"breakdown":{"achievement_quality":70,"skill_depth":50,"research_impact":30,"innovation_mindset":20,"leadership_potential":10},
        "percentile":"top 25%","score_reasoning":"Good foundation, keep building.","improvement_areas":["Publish research","Lead a project"],"badge":"Explorer"})


async def generate_career_roadmap(student: dict, achievements: list) -> dict:
    sys = "You are CareerNav AI. Generate personalized career roadmaps. JSON only."
    prompt = f"""Career roadmap for:
{student.get('name')} | {student.get('department')} | Year {student.get('year')}
Skills: {', '.join(student.get('skills',[]))}
Interests: {', '.join(student.get('interests',[]))}

JSON:
{{"primary_career_path":"string","current_level":"Beginner/Intermediate/Advanced","time_to_job_ready":"X months",
"immediate_actions":[{{"action":"string","why":"string","timeline":"string"}}],
"skill_gaps":[{{"skill":"string","priority":"High/Medium","resource":"string"}}],
"milestones":[{{"month":1,"goal":"string","outcome":"string"}}],
"recommended_projects":["3 ideas"],"salary_outlook":{{"fresher":"X LPA","3_years":"Y LPA"}},
"motivational_note":"1 sentence"}}"""
    raw = await call_llama(prompt, sys)
    roadmap = parse(raw, {"primary_career_path":"Software Engineer","current_level":"Intermediate","time_to_job_ready":"6 months",
        "immediate_actions":[{"action":"Build portfolio project","why":"Employers need proof","timeline":"4 weeks"}],
        "skill_gaps":[{"skill":"System Design","priority":"High","resource":"Grokking System Design"}],
        "milestones":[{"month":3,"goal":"Complete 2 projects","outcome":"Portfolio ready"}],
        "recommended_projects":["AI chatbot","REST API service","ML pipeline"],"salary_outlook":{"fresher":"6-10 LPA","3_years":"15-25 LPA"},
        "motivational_note":"Your technical foundation is strong — execution is all that's left."})

    # Normalize recommended_projects — AI sometimes returns [{idea:"..."}, ...] instead of ["..."]
    def _to_str(v):
        if isinstance(v, str): return v
        if isinstance(v, dict): return next(iter(v.values()), "") if v else ""
        return str(v)

    roadmap["recommended_projects"] = [_to_str(p) for p in roadmap.get("recommended_projects", [])]

    # Normalize string fields in milestones
    for m in roadmap.get("milestones", []):
        m["goal"] = _to_str(m.get("goal", ""))
        m["outcome"] = _to_str(m.get("outcome", ""))

    # Normalize string fields in immediate_actions
    for a in roadmap.get("immediate_actions", []):
        a["action"] = _to_str(a.get("action", ""))
        a["why"] = _to_str(a.get("why", ""))
        a["timeline"] = _to_str(a.get("timeline", ""))

    # Normalize skill_gaps
    for g in roadmap.get("skill_gaps", []):
        g["skill"] = _to_str(g.get("skill", ""))
        g["resource"] = _to_str(g.get("resource", ""))

    # Normalize top-level string fields
    for field in ("primary_career_path", "current_level", "time_to_job_ready", "motivational_note"):
        if field in roadmap:
            roadmap[field] = _to_str(roadmap[field])

    return roadmap


async def chat_with_ai(question: str, student: dict, current_page: str = "") -> str:
    page_ctx = f"\nUser is currently viewing the '{current_page}' page." if current_page else ""
    sys = f"""You are CIT RISE AI Assistant — helpful mentor for college students.{page_ctx}
Student: {student.get('name')} | {student.get('department')} | RISE Score: {student.get('rise_score',0)}
Skills: {', '.join(student.get('skills',[]))}
Be concise, practical, motivating. Under 150 words."""
    return await call_llama(question, sys)


async def generate_daily_challenge(student: dict) -> dict:
    sys = "You are CIT RISE Daily Challenge AI. Create one focused multiple-choice question. JSON only."
    skills = ", ".join(student.get("skills", [])[:3]) or "Python"
    dept = student.get("department", "CSE")
    prompt = f"""Create a practical multiple-choice question for a {dept} student with skills: {skills}.
The question should test career-relevant knowledge (DSA, system design, CS fundamentals, or domain skills).

Return JSON only:
{{"question":"string","options":["A: option","B: option","C: option","D: option"],"correct":"A","explanation":"1-2 sentences explaining why the answer is correct"}}"""
    raw = await call_llama(prompt, sys)
    return parse(raw, {
        "question": "Which time complexity describes a binary search algorithm?",
        "options": ["A: O(n)", "B: O(log n)", "C: O(n²)", "D: O(1)"],
        "correct": "B",
        "explanation": "Binary search halves the search space each iteration, giving O(log n) time complexity."
    })


async def generate_admin_insights(users_db: dict, achievements_db: dict) -> dict:
    sys = "You are CIT RISE Admin Intelligence AI. JSON only."
    students = [u for u in users_db.values() if u.get("role") == "student"]
    depts = {}
    for s in students:
        d = s.get("department","Unknown"); depts[d] = depts.get(d,0)+1
    prompt = f"""Analyze campus innovation data.
Students: {len(students)}, Achievements: {len(achievements_db)}, Depts: {json.dumps(depts)}
Avg RISE: {sum(s.get('rise_score',0) for s in students)//max(len(students),1)}

JSON:
{{"executive_summary":"2 sentences","innovation_health_score":75,
"key_insights":[{{"insight":"string","impact":"High/Medium/Low","action":"string"}}],
"talent_segments":{{"research_potential":30,"startup_potential":20,"placement_ready":50}},
"recommendations":["3 items"],"naac_nirf_highlight":"1 sentence","risk_areas":["list"]}}"""
    raw = await call_llama(prompt, sys)
    return parse(raw, {"executive_summary":"Innovation ecosystem growing steadily.","innovation_health_score":70,
        "key_insights":[{"insight":"CSE AI leads innovation","impact":"High","action":"Replicate model in other depts"}],
        "talent_segments":{"research_potential":30,"startup_potential":20,"placement_ready":50},
        "recommendations":["Launch inter-dept hackathon","Fast-track top scorers","Alumni mentoring program"],
        "naac_nirf_highlight":"Institution demonstrates strong student innovation culture.","risk_areas":["First-years not onboarded"]})


async def analyze_github(username: str) -> dict:
    async with httpx.AsyncClient(timeout=15.0) as c:
        ur = await c.get(f"https://api.github.com/users/{username}", headers={"Accept":"application/vnd.github+json"})
        if ur.status_code == 404: return {"error": f"GitHub user '{username}' not found."}
        if ur.status_code != 200: return {"error": "GitHub API unavailable."}
        profile = ur.json()
        rr = await c.get(f"https://api.github.com/users/{username}/repos",
            params={"sort":"stars","per_page":20}, headers={"Accept":"application/vnd.github+json"})
        repos = rr.json() if rr.status_code == 200 else []
    repos = [{"name":r.get("name"),"description":r.get("description") or "","language":r.get("language") or "Unknown",
              "stars":r.get("stargazers_count",0),"forks":r.get("forks_count",0)} for r in repos if not r.get("fork")]
    langs = list({r["language"] for r in repos if r["language"] != "Unknown"})
    stars = sum(r["stars"] for r in repos)
    raw = {"username":username,"name":profile.get("name") or username,"public_repos":profile.get("public_repos",0),
           "followers":profile.get("followers",0),"total_stars":stars,"languages_used":langs,"top_repos":repos[:8]}
    sys = "Analyze a GitHub profile for CIT RISE. JSON only."
    prompt = f"""Analyze:\n{json.dumps(raw,indent=2)}\n
JSON: {{"developer_level":"Beginner/Intermediate/Advanced","primary_domain":"string","detected_skills":["list"],
"project_highlights":["2-3 sentences"],"open_source_score":75,"career_readiness":"Internship Ready/Junior Ready/Mid-level Ready",
"github_summary":"2 sentences","strengths":["list"],"suggestions":["2 items"]}}"""
    r = await call_llama(prompt, sys)
    ai = parse(r, {"developer_level":"Intermediate","primary_domain":langs[0] if langs else "General",
        "detected_skills":langs,"project_highlights":[repos[0]["name"] if repos else "No repos"],
        "open_source_score":min(stars*5,100),"career_readiness":"Internship Ready",
        "github_summary":f"Developer with {profile.get('public_repos',0)} repos.","strengths":["Consistent","Diverse"],
        "suggestions":["Add READMEs","Contribute to OSS"]})
    return {"raw":raw,"ai_analysis":ai}


async def analyze_leetcode(username: str) -> dict:
    q = """query($username:String!){matchedUser(username:$username){submitStats{acSubmissionNum{difficulty count}}badges{name}}
    userContestRanking(username:$username){rating topPercentage}}"""
    async with httpx.AsyncClient(timeout=15.0) as c:
        res = await c.post("https://leetcode.com/graphql",json={"query":q,"variables":{"username":username}},
            headers={"Content-Type":"application/json","Referer":"https://leetcode.com"})
    if res.status_code != 200: return {"error": "LeetCode API unavailable."}
    d = res.json(); ud = d.get("data",{}).get("matchedUser")
    if not ud: return {"error": f"LeetCode user '{username}' not found."}
    sm = {s["difficulty"]:s["count"] for s in ud.get("submitStats",{}).get("acSubmissionNum",[])}
    cr = d.get("data",{}).get("userContestRanking") or {}
    raw = {"username":username,"solved":{"easy":sm.get("Easy",0),"medium":sm.get("Medium",0),"hard":sm.get("Hard",0),"total":sm.get("All",0)},
           "contest_rating":cr.get("rating"),"top_percentage":cr.get("topPercentage")}
    sys = "Generate DSA study plan from LeetCode stats. JSON only."
    total = raw["solved"]["total"]
    prompt = f"""Stats:\n{json.dumps(raw)}\n
JSON: {{"dsa_level":"Beginner/Intermediate/Advanced","strong_areas":["list"],"weak_areas":["list"],
"interview_readiness":"Not Ready/Getting There/Interview Ready/FAANG Ready",
"study_plan":[{{"week":1,"focus":"topic","target":"X problems","reason":"why"}}],
"next_milestone":"string","company_targets":["list"],"lc_summary":"2 sentences"}}"""
    r = await call_llama(prompt, sys)
    ai = parse(r, {"dsa_level":"Intermediate" if total>100 else "Beginner","strong_areas":["Arrays","Strings"],
        "weak_areas":["DP","Graphs"],"interview_readiness":"Getting There" if total>50 else "Not Ready",
        "study_plan":[{"week":1,"focus":"Two Pointers","target":"15 problems","reason":"High interview frequency"}],
        "next_milestone":f"Reach {total+50} total solved","company_targets":["Product startups","Service companies"],
        "lc_summary":f"Solved {total} total. Consistent practice recommended."})
    return {"raw":raw,"ai_analysis":ai}


async def analyze_idea(title: str, description: str) -> dict:
    """
    AI analysis of student innovation idea
    - Categorizes idea
    - Scores feasibility (0-100)
    - Suggests relevant mentors (from mentors_db keys)
    - Returns structured analysis for idea submission
    """
    sys = "You are CIT RISE Ideas AI. Analyze innovation ideas for feasibility and category. JSON only."
    prompt = f"""Analyze this student innovation idea:

Title: {title}
Description: {description}

Provide:
1. Category (e.g., Education Tech, IoT & Sustainability, FinTech, HealthTech, Social Impact, etc.)
2. Feasibility score 0-100 (considering scope, timeline, resources in college context)
3. 2-3 relevant mentor field suggestions (from: ML, Full Stack, Product, Robotics)
4. Brief feasibility reasoning

Return JSON only:
{{
    "category": "string",
    "feasibility_score": 75,
    "mentor_field_suggestions": ["ML", "Full Stack"],
    "feasibility_reasoning": "string",
    "implementation_complexity": "Low/Medium/High",
    "potential_impact": "High/Medium/Low",
    "suggested_first_steps": ["step 1", "step 2", "step 3"]
}}"""
    
    raw = await call_llama(prompt, sys)
    result = parse(raw, {
        "category": "Innovation",
        "feasibility_score": 60,
        "mentor_field_suggestions": ["Full Stack"],
        "feasibility_reasoning": "Moderate complexity idea. Good learning opportunity.",
        "implementation_complexity": "Medium",
        "potential_impact": "Medium",
        "suggested_first_steps": ["Research similar projects", "Create MVP plan", "Start with MVP"]
    })
    
    # Map mentor field suggestions to actual mentors from mentors_db
    # This is a simplified mapping
    from config.store import mentors_db
    mentor_map = {
        "ML": "m1",
        "Full Stack": "m2", 
        "Product": "m3",
        "Robotics": "m4"
    }
    
    suggested_mentor_ids = []
    for field in result.get("mentor_field_suggestions", []):
        if field in mentor_map:
            mentor_id = mentor_map[field]
            if mentor_id in mentors_db:
                suggested_mentor_ids.append(mentor_id)
    
    # If no mentors found, use first 2 mentors
    if not suggested_mentor_ids and mentors_db:
        suggested_mentor_ids = list(mentors_db.keys())[:2]
    
    result["mentor_suggestions"] = suggested_mentor_ids
    
    return result
