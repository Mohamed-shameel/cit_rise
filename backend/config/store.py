from datetime import datetime

users_db: dict = {}
achievements_db: dict = {}
mentors_db: dict = {}
opportunities_db: dict = {}

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
              "domain":"AI/ML","deadline":"2026-04-01","type":"internship","posted_by":"admin","created_at":datetime.utcnow().isoformat()},
        "o2":{"opportunity_id":"o2","title":"Startup Pitch - NASSCOM","description":"Present your startup. Winner gets Rs.5L seed funding.",
              "domain":"Startup","deadline":"2026-03-20","type":"competition","posted_by":"admin","created_at":datetime.utcnow().isoformat()},
    })

seed()
