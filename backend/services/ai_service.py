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


# ---------------------------------------
# LLM CALL
# ---------------------------------------

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


# ---------------------------------------
# JSON PARSER
# ---------------------------------------

def parse(raw: str, fallback: dict) -> dict:

    try:
        clean = raw.strip()

        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]

        return json.loads(clean.strip())

    except Exception as e:
        print("[AI JSON PARSE ERROR]", e)
        print("[RAW RESPONSE]", raw[:500])
        return fallback


# ---------------------------------------
# STUDENT PROFILE FROM RESUME
# ---------------------------------------

async def generate_student_profile(resume_text: str, github: Optional[str] = None) -> dict:

    sys = "You are an expert career advisor. Extract structured student profile from a resume. JSON only."

    gh = f"\nGitHub: {github}" if github else ""

    prompt = f"""
Analyze the following student resume.{gh}

Resume:
{resume_text[:3000]}

Return JSON:

{{
"name":"string",
"department":"CSE/ECE/MECH/IT/EEE/CSE AI",
"year":2,
"skills":["list"],
"interests":["list"],
"strengths":["3 phrases"],
"profile_summary":"2-3 sentences",
"innovation_potential":"High/Medium/Low",
"suggested_roles":["3 roles"],

"resume_suggestions":[
"add measurable impact metrics",
"include GitHub project links",
"improve technical skills section"
]
}}
"""

    raw = await call_llama(prompt, sys)

    return parse(raw, {
        "name": "Student",
        "department": "CSE",
        "year": 2,
        "skills": ["Python"],
        "interests": ["Technology"],
        "strengths": ["Analytical", "Fast learner", "Team player"],
        "profile_summary": "Motivated student with technical potential.",
        "innovation_potential": "Medium",
        "suggested_roles": ["Software Engineer","ML Engineer","Web Developer"],
        "resume_suggestions":[
            "Add quantified achievements",
            "Link GitHub projects",
            "Highlight core technologies"
        ]
    })


# ---------------------------------------
# RISE SCORE ENGINE
# ---------------------------------------

async def calculate_rise_score(student: dict, achievements: list) -> dict:

    sys = "You are CIT RISE Score AI evaluating student innovation potential."

    ach = "\n".join(
        [f"- {a['title']} ({a['type']})" for a in achievements]
    ) or "No achievements yet."

    prompt = f"""
Evaluate this student using CIT RISE Innovation Score (0–500).

Student:
{student.get('name')} | {student.get('department')} | Year {student.get('year')}

Skills:
{', '.join(student.get('skills',[]))}

Achievements:
{ach}

Return JSON:

{{
"total_score":200,

"breakdown":{{
"achievement_quality":80,
"skill_depth":60,
"research_impact":30,
"innovation_mindset":20,
"leadership_potential":10
}},

"percentile":"top X%",

"score_reasoning":"2 sentences",

"improvement_areas":[
"publish technical blogs",
"contribute to open source"
],

"badge":"Pioneer/Innovator/Explorer/Starter"
}}
"""

    raw = await call_llama(prompt, sys)

    return parse(raw, {
        "total_score":180,
        "breakdown":{
            "achievement_quality":70,
            "skill_depth":50,
            "research_impact":30,
            "innovation_mindset":20,
            "leadership_potential":10
        },
        "percentile":"top 25%",
        "score_reasoning":"Good foundation with room for research impact.",
        "improvement_areas":["Publish research","Lead project teams"],
        "badge":"Explorer"
    })


# ---------------------------------------
# CAREER ROADMAP
# ---------------------------------------

async def generate_career_roadmap(student: dict, github: dict = None, leetcode: dict = None) -> dict:

    # ── Extract context from GitHub + LeetCode analyses ──────────────────────
    github   = github   or student.get("github_analysis",   {})
    leetcode = leetcode or student.get("leetcode_analysis", {})

    skills    = student.get("skills",    [])
    interests = student.get("interests", [])

    github_domain       = github.get("primary_domain",      "Software")
    github_level        = github.get("developer_level",     "Intermediate")
    github_repos        = github.get("public_repos",        0)
    github_stars        = github.get("total_stars",         0)
    career_readiness    = github.get("career_readiness",    "Unknown")

    leetcode_level      = leetcode.get("dsa_level",          "Intermediate")
    interview_readiness = leetcode.get("interview_readiness","Getting There")
    leetcode_solved     = leetcode.get("solved_total",       0)
    company_targets     = leetcode.get("company_targets",    ["Startups"])

    rise_score = student.get("rise_score", 0)
    # ─────────────────────────────────────────────────────────────────────────

    sys = """You are CareerNav AI — an expert software career mentor.

You generate personalized roadmaps for students based on:
- skills
- GitHub portfolio analysis
- LeetCode performance
- academic background
- interests

Return STRICT JSON only. No explanation, no markdown, no extra text."""

    prompt = f"""Student profile:

Name: {student.get('name')}
Department: {student.get('department')}
Year: {student.get('year')}
RISE Score: {rise_score}

Skills: {', '.join(skills) if skills else 'None listed'}
Interests: {', '.join(interests) if interests else 'Not specified'}

GitHub Intelligence:
- Domain: {github_domain}
- Developer Level: {github_level}
- Repos: {github_repos} | Stars: {github_stars}
- Career Readiness: {career_readiness}

LeetCode Intelligence:
- DSA Level: {leetcode_level}
- Interview Readiness: {interview_readiness}
- Total Solved: {leetcode_solved}
- Company Targets: {', '.join(company_targets)}

Create a realistic career roadmap perfectly aligned with the student's actual GitHub domain and LeetCode level.
Be specific about the domain (ML, Web, Systems, Data) based on their GitHub domain.
Do not give generic advice.

Return JSON in this EXACT format:

{{"primary_career_path":"ML Engineer | Software Engineer | Full Stack Developer | Data Scientist","current_level":"Beginner | Intermediate | Advanced","time_to_job_ready":"X months","immediate_actions":[{{"action":"specific step","why":"reason","timeline":"timeframe"}},{{"action":"specific step","why":"reason","timeline":"timeframe"}},{{"action":"specific step","why":"reason","timeline":"timeframe"}}],"skill_gaps":[{{"skill":"Dynamic Programming","priority":"High","resource":"LeetCode DP track"}},{{"skill":"System Design","priority":"Medium","resource":"Grokking System Design"}}],"milestones":[{{"month":1,"goal":"specific goal","outcome":"measurable outcome"}},{{"month":2,"goal":"specific goal","outcome":"measurable outcome"}},{{"month":3,"goal":"specific goal","outcome":"measurable outcome"}}],"recommended_projects":["project idea 1","project idea 2","project idea 3"],"salary_outlook":{{"fresher":"6-10 LPA","3_years":"15-25 LPA"}},"motivational_note":"1 encouraging sentence tailored to this student"}}"""

    raw = await call_llama(prompt, sys)

    roadmap = parse(raw, {
        "primary_career_path": f"{github_domain} Engineer",
        "current_level":       github_level or "Intermediate",
        "time_to_job_ready":   "5 months",
        "immediate_actions": [
            {"action": f"Solve 20 Dynamic Programming problems on LeetCode", "why": "DP is the #1 interview topic at product companies", "timeline": "3 weeks"},
            {"action": f"Build a portfolio project in {github_domain}", "why": "Demonstrate domain expertise to recruiters", "timeline": "4 weeks"},
            {"action": "Study System Design fundamentals", "why": "Required for SDE-1 interviews at product companies", "timeline": "2 weeks"}
        ],
        "skill_gaps": [
            {"skill": "Dynamic Programming", "priority": "High",   "resource": "LeetCode DP Study Plan"},
            {"skill": "System Design",        "priority": "Medium", "resource": "Grokking System Design"},
            {"skill": "Graph Algorithms",     "priority": "High",   "resource": "LeetCode Graph problems"}
        ],
        "milestones": [
            {"month": 1, "goal": "Strengthen DSA",          "outcome": f"Solve {leetcode_solved + 30} total LeetCode problems"},
            {"month": 2, "goal": "Build portfolio project", "outcome": f"Deploy a {github_domain}-domain project on GitHub"},
            {"month": 3, "goal": "Interview preparation",   "outcome": "Complete 10 mock interviews"}
        ],
        "recommended_projects": [
            f"AI-powered Resume Analyzer ({github_domain})",
            "REST API Backend with FastAPI + PostgreSQL",
            "Real-time Dashboard with WebSocket"
        ],
        "salary_outlook": {"fresher": "6-10 LPA", "3_years": "15-25 LPA"},
        "motivational_note": f"You've got {github_repos} repos and {leetcode_solved} problems solved — that's a strong foundation. Keep building!"
    })

    return roadmap


# ---------------------------------------
# AI ASSISTANT
# ---------------------------------------

async def chat_with_ai(question: str, student: dict, current_page: str = "") -> str:

    page_ctx = f"\nUser is currently viewing: {current_page}" if current_page else ""

    sys = f"""You are CIT RISE AI Career Mentor.

Be:
- polite
- structured
- concise

Student:
Name: {student.get('name')}
Department: {student.get('department')}
RISE Score: {student.get('rise_score',0)}
Skills: {', '.join(student.get('skills',[]))}
{page_ctx}

Answer format:

### Insight
Explain the concept.

### Recommendation
Give actionable advice.

### Next Step
Tell the student exactly what to do next.

Maximum 120 words."""

    return await call_llama(question, sys)


# ---------------------------------------
# GITHUB ANALYSIS
# ---------------------------------------

async def analyze_github(username: str) -> dict:

    async with httpx.AsyncClient(timeout=15.0) as c:

        ur = await c.get(
            f"https://api.github.com/users/{username}",
            headers={"Accept":"application/vnd.github+json"}
        )

        if ur.status_code == 404:
            return {"error": f"GitHub user '{username}' not found."}

        profile = ur.json()

        rr = await c.get(
            f"https://api.github.com/users/{username}/repos",
            params={"sort":"stars","per_page":20}
        )

        repos = rr.json() if rr.status_code == 200 else []

    repos = [
        {
            "name": r.get("name"),
            "description": r.get("description") or "",
            "language": r.get("language") or "Unknown",
            "stars": r.get("stargazers_count",0)
        }
        for r in repos if not r.get("fork")
    ]

    langs = list({r["language"] for r in repos if r["language"]!="Unknown"})

    stars = sum(r["stars"] for r in repos)

    raw = {
        "username":username,
        "public_repos":profile.get("public_repos",0),
        "followers":profile.get("followers",0),
        "total_stars":stars,
        "languages_used":langs,
        "top_repos":repos[:8]
    }

    sys = """You are a senior software engineer reviewing a student's GitHub portfolio.

Your job:
1. Evaluate the developer level
2. Detect technical skills
3. Identify strengths
4. Identify weaknesses
5. Provide clear improvement recommendations
6. Suggest projects to improve their portfolio

Return STRICT JSON only. No explanation, no markdown, no extra text."""

    prompt = f"""Analyze the GitHub profile below.

{json.dumps(raw, indent=2)}

Return JSON in this EXACT format:

{{"developer_level":"Beginner | Intermediate | Advanced","primary_domain":"Web | AI/ML | Systems | DevOps | Data","detected_skills":["skill1","skill2"],"portfolio_strengths":["strength 1","strength 2"],"portfolio_weaknesses":["weakness 1","weakness 2"],"improvement_recommendations":[{{"action":"specific improvement","reason":"why this matters","example_project":"project idea"}}],"career_readiness":"Not Ready | Internship Ready | Junior Ready","github_summary":"2 sentences"}}"""

    r = await call_llama(prompt, sys)

    ai = parse(r, {
        "developer_level": "Intermediate",
        "primary_domain": langs[0] if langs else "General",
        "detected_skills": langs[:5],
        "portfolio_strengths": ["Active GitHub presence", "Diverse repository topics"],
        "portfolio_weaknesses": ["No README documentation", "Limited collaborative projects"],
        "improvement_recommendations": [
            {"action": "Add detailed README to each repo", "reason": "Recruiters judge repos by documentation", "example_project": "Create a portfolio README"},
            {"action": "Contribute to open source", "reason": "Shows collaborative development skills", "example_project": "Pick a beginner-friendly OSS project"}
        ],
        "career_readiness": "Internship Ready",
        "github_summary": f"Developer with {raw.get('public_repos',0)} repositories and {stars} total stars."
    })

    return {"raw":raw,"ai_analysis":ai}


# ---------------------------------------
# LEETCODE ANALYSIS
# ---------------------------------------

async def analyze_leetcode(username: str) -> dict:

    q = """query($username:String!){
    matchedUser(username:$username){
    submitStats{acSubmissionNum{difficulty count}}
    }
    }"""

    async with httpx.AsyncClient(timeout=15.0) as c:

        res = await c.post(
            "https://leetcode.com/graphql",
            json={"query":q,"variables":{"username":username}},
            headers={"Content-Type":"application/json"}
        )

    if res.status_code != 200:
        return {"error":"LeetCode API unavailable."}

    d = res.json()

    ud = d.get("data",{}).get("matchedUser")

    if not ud:
        return {"error":f"LeetCode user '{username}' not found."}

    sm = {s["difficulty"]:s["count"] for s in ud["submitStats"]["acSubmissionNum"]}

    raw = {
        "username":username,
        "solved":{
            "easy":sm.get("Easy",0),
            "medium":sm.get("Medium",0),
            "hard":sm.get("Hard",0),
            "total":sm.get("All",0)
        }
    }

    # ── Pre-processing diagnostics (before calling AI) ───────────────────────
    total  = raw["solved"]["total"]
    easy   = raw["solved"]["easy"]
    medium = raw["solved"]["medium"]
    hard   = raw["solved"]["hard"]

    # Base level from problem count
    if total < 100:
        base_level = "Beginner"
    elif total < 300:
        base_level = "Intermediate"
    else:
        base_level = "Advanced"

    # Detect imbalance / weakness signals
    detected_weak = []
    if hard < 20:
        detected_weak.append(f"Hard problems (only {hard} solved)")
    if total > 50 and medium < easy * 0.5:
        detected_weak.append("Medium-level problems (low medium/easy ratio)")

    # Core interview topics not verifiable from solve count alone
    core_topic_gaps = ["Dynamic Programming", "Graphs", "Backtracking", "Tree Algorithms"]
    # ────────────────────────────────────────────────────────────────────

    sys = """You are a senior Data Structures & Algorithms mentor evaluating a student's LeetCode profile.

Your goals:
- Provide a fair skill level assessment
- Identify conceptual gaps
- Give motivating and constructive feedback
- Provide a practical improvement roadmap

Return STRICT JSON only. No explanation, no markdown, no extra text."""

    prompt = f"""Student LeetCode stats:

Total solved: {total}
Easy: {easy}
Medium: {medium}
Hard: {hard}

Base level from problem count: {base_level}

Potential weak areas detected:
{detected_weak}

Important interview topics not verified from count alone:
{core_topic_gaps}

Evaluation rules:
1. If the student solved many problems but lacks hard problems or core topics (DP, Graphs, Backtracking), classify them as "Intermediate - Concept Gaps".
2. Be encouraging and constructive.
3. Use {base_level} as a starting point but adjust if imbalances exist.

Return JSON in this EXACT format:

{{"dsa_level":"Beginner | Intermediate | Intermediate - Concept Gaps | Advanced","level_explanation":"short explanation of why this level was assigned","strong_areas":["topic"],"weak_areas":["Dynamic Programming","Graphs","Backtracking"],"concept_gaps":["DP state transition","Graph shortest path","Backtracking recursion"],"interview_readiness":"Not Ready | Getting There | Interview Ready","improvement_plan":[{{"focus_topic":"Dynamic Programming","reason":"DP is frequently asked in product-company interviews","target_problems":15}},{{"focus_topic":"Graphs","reason":"Graph algorithms appear in many technical interviews","target_problems":12}}],"weekly_practice_plan":[{{"week":1,"focus":"Dynamic Programming basics","target":"10 problems"}},{{"week":2,"focus":"Graph BFS/DFS","target":"10 problems"}}],"milestone_goals":["Solve 20 dynamic programming problems","Solve 15 graph problems"],"company_targets":["Product companies","High-growth startups"],"lc_summary":"encouraging 2-sentence summary"}}"""

    r = await call_llama(prompt, sys)

    ai = parse(r, {
        "dsa_level": f"{base_level} - Concept Gaps" if hard < 20 and total > 100 else base_level,
        "level_explanation": f"Solved {total} total problems with strong easy/medium coverage, but only {hard} hard problems and key algorithm topics like DP and Graphs need attention.",
        "strong_areas": ["Array manipulation", "String problems", "Basic problem-solving"],
        "weak_areas": ["Dynamic Programming", "Graphs", "Backtracking"],
        "concept_gaps": ["DP state transition design", "Graph shortest path algorithms", "Backtracking recursion patterns"],
        "interview_readiness": "Getting There" if total > 100 else "Not Ready",
        "improvement_plan": [
            {"focus_topic": "Dynamic Programming", "reason": "Frequently asked in product-company interviews", "target_problems": 15},
            {"focus_topic": "Graph Algorithms", "reason": "BFS/DFS appear in most technical interviews", "target_problems": 12},
            {"focus_topic": "Backtracking", "reason": "Required for combinations, permutations and constraint problems", "target_problems": 10}
        ],
        "weekly_practice_plan": [
            {"week": 1, "focus": "DP Basics (Fibonacci, Knapsack)", "target": "10 problems"},
            {"week": 2, "focus": "Graph BFS/DFS", "target": "10 problems"},
            {"week": 3, "focus": "Hard DP (LCS, LIS, Matrix DP)", "target": "8 problems"},
            {"week": 4, "focus": "Backtracking & Recursion", "target": "8 problems"}
        ],
        "milestone_goals": [
            f"Reach {total + 50} total solved problems",
            "Solve 20 dynamic programming problems",
            "Solve 15 graph problems",
            "Reach 30 hard problems solved"
        ],
        "company_targets": ["Product companies", "High-growth startups"],
        "lc_summary": f"You've solved {total} problems — that's real dedication! Focus on DP and graph algorithms next to unlock interview readiness at top product companies."
    })

    return {"raw":raw,"ai_analysis":ai}


# ---------------------------------------
# DAILY CHALLENGE
# ---------------------------------------

async def generate_daily_challenge(student: dict) -> dict:

    sys = "You are CIT RISE Daily Challenge AI. Create one focused multiple-choice question. JSON only."

    skills = ", ".join(student.get("skills", [])[:3]) or "Python"
    dept = student.get("department", "CSE")

    prompt = f"""
Create a practical multiple-choice question for a {dept} student with skills: {skills}.
Test career-relevant knowledge (DSA, system design, CS fundamentals, or domain skills).

Return JSON:

{{
"question":"string",
"options":["A: option","B: option","C: option","D: option"],
"correct":"A",
"explanation":"1-2 sentences explaining why the answer is correct"
}}
"""

    raw = await call_llama(prompt, sys)

    return parse(raw, {
        "question": "Which time complexity describes binary search?",
        "options": ["A: O(n)", "B: O(log n)", "C: O(n\u00b2)", "D: O(1)"],
        "correct": "B",
        "explanation": "Binary search halves the search space each iteration, giving O(log n) complexity."
    })


# ---------------------------------------
# ADMIN INSIGHTS
# ---------------------------------------

async def generate_admin_insights(users_db: dict, achievements_db: dict) -> dict:

    sys = "You are CIT RISE Admin Intelligence AI. JSON only."

    students = [u for u in users_db.values() if u.get("role") == "student"]

    depts = {}
    for s in students:
        d = s.get("department", "Unknown")
        depts[d] = depts.get(d, 0) + 1

    avg_score = sum(s.get("rise_score", 0) for s in students) // max(len(students), 1)

    prompt = f"""
Analyze campus innovation data.

Students: {len(students)}
Achievements: {len(achievements_db)}
Departments: {json.dumps(depts)}
Average RISE Score: {avg_score}

Return JSON:

{{
"executive_summary":"2 sentences",
"innovation_health_score":75,

"key_insights":[
{{"insight":"string","impact":"High/Medium/Low","action":"string"}}
],

"talent_segments":{{
"research_potential":30,
"startup_potential":20,
"placement_ready":50
}},

"recommendations":["item 1","item 2","item 3"],

"naac_nirf_highlight":"1 sentence",

"risk_areas":["risk 1","risk 2"]
}}
"""

    raw = await call_llama(prompt, sys)

    return parse(raw, {
        "executive_summary": "Innovation ecosystem growing steadily across departments.",
        "innovation_health_score": 70,
        "key_insights": [
            {"insight": "CSE AI leads innovation", "impact": "High", "action": "Replicate model in other depts"}
        ],
        "talent_segments": {"research_potential": 30, "startup_potential": 20, "placement_ready": 50},
        "recommendations": ["Launch inter-dept hackathon", "Fast-track top scorers", "Alumni mentoring program"],
        "naac_nirf_highlight": "Institution demonstrates strong student innovation culture.",
        "risk_areas": ["First-years not onboarded", "Low research output in non-CS depts"]
    })


# ---------------------------------------
# IDEA ANALYSIS
# ---------------------------------------

async def analyze_idea(title: str, description: str) -> dict:

    sys = "You are CIT RISE Ideas AI. Analyze innovation ideas for feasibility and category. JSON only."

    prompt = f"""
Analyze this student innovation idea.

Title: {title}
Description: {description}

Return JSON:

{{
"category":"Education Tech / IoT / FinTech / HealthTech / Social Impact / etc.",
"feasibility_score":75,
"mentor_field_suggestions":["ML","Full Stack"],
"feasibility_reasoning":"string",
"implementation_complexity":"Low/Medium/High",
"potential_impact":"High/Medium/Low",
"suggested_first_steps":["step 1","step 2","step 3"]
}}
"""

    raw = await call_llama(prompt, sys)

    result = parse(raw, {
        "category": "Innovation",
        "feasibility_score": 60,
        "mentor_field_suggestions": ["Full Stack"],
        "feasibility_reasoning": "Moderate complexity. Good learning opportunity.",
        "implementation_complexity": "Medium",
        "potential_impact": "Medium",
        "suggested_first_steps": ["Research similar projects", "Create MVP plan", "Build prototype"]
    })

    # Map mentor field suggestions to actual mentor IDs
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

    if not suggested_mentor_ids and mentors_db:
        suggested_mentor_ids = list(mentors_db.keys())[:2]

    result["mentor_suggestions"] = suggested_mentor_ids

    return result