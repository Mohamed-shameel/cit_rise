from datetime import datetime
import uuid

users_db: dict = {}
achievements_db: dict = {}
mentors_db: dict = {}
opportunities_db: dict = {}
user_opportunities: dict = {}  # M2M: user_id + opp_id + status
deduplication_log: dict = {}  # Track merged opportunities
scraper_logs: dict = {}  # Track scraping operations
source_tracking: dict = {}  # Map source_id to opp_id for quick lookup

# Ideas submission system
ideas_db: dict = {}  # key: idea_id, value: {id, student_id, title, description, category, feasibility_score, mentor_suggestions, status, ...}
idea_comments_db: dict = {}  # key: idea_id, value: [{admin_id, comment, timestamp}, ...]
idea_submissions_log: dict = {"total": 0, "categories": {}}  # Analytics

# Mentor chat messages
messages_db: dict = {}  # key: "{student_id}__{mentor_id}", value: [{sender, text, timestamp}]

# Daily challenge state
daily_challenges_db: dict = {}  # key: student_id, value: {question, options, correct, explanation, date, answered, answer_given}

def seed():
    mentors_db.update({
        "m1": {"mentor_id":"m1","name":"Dr. Priya Ramesh","company":"Google DeepMind","domain":"Machine Learning",
               "skills":["Python","TensorFlow","MLOps","Deep Learning","NLP"],"linkedin":"linkedin.com/in/priyaramesh",
               "bio":"10 years in ML research. Alumni CIT 2014.","available":True},
        "m2": {"mentor_id":"m2","name":"Karthik Sundaram","company":"Zoho Corp","domain":"Full Stack Development",
               "skills":["React","Node.js","FastAPI","PostgreSQL","Docker"],"linkedin":"linkedin.com/in/karthiksundaram",
               "bio":"Senior Engineer at Zoho. Alumni CIT 2016.","available":True},
        "m3": {"mentor_id":"m3","name":"Ananya Krishnan","company":"Freshworks","domain":"Product & Startups",
               "skills":["Product Management","UX","Growth Hacking","Fundraising"],"linkedin":"linkedin.com/in/ananyakrishnan",
               "bio":"Built and exited a SaaS startup. Now PM at Freshworks. Alumni CIT 2013.","available":True},
        "m4": {"mentor_id":"m4","name":"Rahul Nair","company":"ISRO","domain":"Robotics & Embedded",
               "skills":["Robotics","Embedded C","ROS","IoT","Control Systems"],"linkedin":"linkedin.com/in/rahulnair",
               "bio":"Robotics engineer at ISRO. Alumni CIT 2015.","available":True},
    })
    users_db["student_demo"] = {
        "user_id":"student_demo","name":"Shameel Ahmed","email":"shameel@citchennai.net",
        "role":"student","department":"CSE AI","year":3,
        "skills":["Python","Machine Learning","React","FastAPI"],
        "interests":["AI","Startups","Open Source"],
        "github":"github.com/shameel","linkedin":"linkedin.com/in/shameel",
        "rise_score":210,
        "rise_score_breakdown":{"achievement_quality":80,"skill_depth":60,"research_impact":40,"innovation_mindset":20,"leadership_potential":10},
        "rise_score_meta":{"percentile":"top 15%","reasoning":"SIH win + IEEE paper at Year 3 is exceptional.",
                           "badge":"Innovator","improvement_areas":["Start a campus club","Contribute to open source"]},
        "ai_profile_summary":"Highly motivated CSE AI student with strong ML skills and proven research track record.",
        "innovation_potential":"High","suggested_roles":["ML Engineer","AI Researcher","Full Stack Developer"],
        "career_roadmap":None,"created_at":datetime.utcnow().isoformat()
    }
    achievements_db.update({
        "ach1":{"achievement_id":"ach1","student_id":"student_demo","title":"Winner - Smart India Hackathon 2024",
                "type":"hackathon","description":"Built AI-powered waste management system",
                "date":"2024-09-15","verified":True,"created_at":datetime.utcnow().isoformat()},
        "ach2":{"achievement_id":"ach2","student_id":"student_demo","title":"Research Paper - NLP for Regional Languages",
                "type":"research","description":"Published at IEEE conference on Tamil NLP",
                "date":"2024-11-20","verified":True,"created_at":datetime.utcnow().isoformat()},
    })
    opportunities_db.update({
        "o1":{"opportunity_id":"o1","title":"AI Research Internship - IIT Madras","description":"Summer internship in NLP lab.",
              "domain":["AI/ML", "Research"],"deadline":"2026-04-01","type":"internship","posted_by":"admin",
              "source":"admin","source_id":"admin_o1","source_url":"","verified":True,
              "company":"IIT Madras","location":"Chennai","salary_range":"₹15,000/month","duration":"3 months",
              "department_fit":["CSE","CSE AI"],"eligibility":{"min_cgpa":3.0,"year":[2,3]},
              "ai_analysis":{"relevance_score":8.5,"difficulty_level":"Medium","learning_value":"High","category_confidence":0.95},
              "created_at":datetime.utcnow().isoformat(),"updated_at":datetime.utcnow().isoformat()},
        "o2":{"opportunity_id":"o2","title":"Startup Pitch - NASSCOM","description":"Present your startup. Winner gets Rs.5L seed funding.",
              "domain":["Startup","Entrepreneurship"],"deadline":"2026-03-20","type":"competition","posted_by":"admin",
              "source":"admin","source_id":"admin_o2","source_url":"","verified":True,
              "company":"NASSCOM","location":"National","salary_range":"₹5,00,000 prize","duration":"1 day event",
              "department_fit":["CSE","CSE AI","IT"],"eligibility":{"min_cgpa":0.0,"year":[1,2,3,4]},
              "ai_analysis":{"relevance_score":7.0,"difficulty_level":"Medium","learning_value":"Medium","category_confidence":0.92},
              "created_at":datetime.utcnow().isoformat(),"updated_at":datetime.utcnow().isoformat()},
    })
    
    # Sample ideas
    ideas_db.update({
        "idea-sample-1": {
            "id": "idea-sample-1",
            "student_id": "student_demo",
            "title": "AI-Powered Tutoring Platform",
            "description": "An intelligent tutoring system that adapts to student learning pace using ML and NLP for personalized learning paths.",
            "category": "Education Tech",
            "feasibility_score": 85,
            "mentor_suggestions": ["Dr. Priya Ramesh"],
            "status": "pending",
            "submitted_at": datetime.utcnow().isoformat(),
            "reviewed_at": None,
            "qr_code_url": "/qr/idea-sample-1.png",
            "rise_score_impact": 0
        },
        "idea-sample-2": {
            "id": "idea-sample-2",
            "student_id": "student_demo",
            "title": "Smart Waste Management IoT",
            "description": "IoT sensors for real-time waste bin monitoring and optimization of collection routes.",
            "category": "IoT & Sustainability",
            "feasibility_score": 72,
            "mentor_suggestions": ["Rahul Nair"],
            "status": "reviewed",
            "submitted_at": "2026-02-15T10:30:00",
            "reviewed_at": "2026-02-20T14:45:00",
            "qr_code_url": "/qr/idea-sample-2.png",
            "rise_score_impact": 20
        },
    })
    
    idea_submissions_log["total"] = len(ideas_db)
    for idea in ideas_db.values():
        cat = idea.get("category", "Other")
        idea_submissions_log["categories"][cat] = idea_submissions_log["categories"].get(cat, 0) + 1

seed()
