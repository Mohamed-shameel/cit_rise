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
        "career_roadmap":None,"created_at":datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None, "score_history": []
    }

    # ── 15 Synthetic Students ──────────────────────────────────────────────────
    users_db["student_001"] = {
        "user_id": "student_001", "name": "Arjun Krishnamurthy",
        "email": "arjun.krishnamurthy@citchennai.net",
        "role": "student", "department": "CSE AI", "year": 3,
        "skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker"],
        "interests": ["ML Research", "Deep Learning", "Open Source"],
        "github": "github.com/arjunkrishnamurthy", "linkedin": "linkedin.com/in/arjunkrishnamurthy",
        "rise_score": 478,
        "rise_score_breakdown": {"achievement_quality": 160, "skill_depth": 140, "research_impact": 100, "innovation_mindset": 50, "leadership_potential": 28},
        "rise_score_meta": {"percentile": "top 1%", "reasoning": "IEEE paper + national hackathon win + Google cert at Year 3 is extraordinary.", "badge": "Visionary", "improvement_areas": ["Lead a student research group", "Publish more papers"]},
        "ai_profile_summary": "Top-ranked CSE-AI student with deep ML expertise and verified research publications.",
        "innovation_potential": "Very High", "suggested_roles": ["ML Research Engineer", "AI Researcher", "MLOps Engineer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": [210, 310, 400, 451, 478]
    }

    users_db["student_002"] = {
        "user_id": "student_002", "name": "Priya Venkatesh",
        "email": "priya.venkatesh@citchennai.net",
        "role": "student", "department": "CSE", "year": 4,
        "skills": ["React", "Node.js", "AWS", "PostgreSQL", "System Design"],
        "interests": ["Web Development", "Open Source", "System Architecture"],
        "github": "github.com/priyavenkatesh", "linkedin": "linkedin.com/in/priyavenkatesh",
        "rise_score": 412,
        "rise_score_breakdown": {"achievement_quality": 130, "skill_depth": 120, "research_impact": 60, "innovation_mindset": 60, "leadership_potential": 42},
        "rise_score_meta": {"percentile": "top 5%", "reasoning": "SIH finalist + industry internship + open source contributions make a strong profile.", "badge": "Innovator", "improvement_areas": ["Publish a technical blog", "Contribute to a major open source project"]},
        "ai_profile_summary": "Final-year CSE student with strong full-stack skills and real-world industry experience.",
        "innovation_potential": "High", "suggested_roles": ["Full Stack Engineer", "Backend Engineer", "Product Engineer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [180, 260, 340, 390, 412]
    }

    users_db["student_003"] = {
        "user_id": "student_003", "name": "Mohammed Farhan",
        "email": "mohammed.farhan@citchennai.net",
        "role": "student", "department": "ECE", "year": 3,
        "skills": ["Embedded C", "VLSI", "Arduino", "FPGA", "IoT"],
        "interests": ["Embedded Systems", "VLSI Design", "Patent Innovation"],
        "github": "github.com/mohammedfarhan", "linkedin": "linkedin.com/in/mohammedfarhan",
        "rise_score": 367,
        "rise_score_breakdown": {"achievement_quality": 130, "skill_depth": 100, "research_impact": 70, "innovation_mindset": 45, "leadership_potential": 22},
        "rise_score_meta": {"percentile": "top 8%", "reasoning": "Patent filed plus state-level award is exceptional for an ECE student.", "badge": "Innovator", "improvement_areas": ["Develop IoT project on GitHub", "Attend international conferences"]},
        "ai_profile_summary": "ECE innovator with a filed patent and state-level recognition in embedded systems.",
        "innovation_potential": "High", "suggested_roles": ["Embedded Systems Engineer", "VLSI Designer", "IoT Developer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": [150, 220, 300, 350, 367]
    }

    users_db["student_004"] = {
        "user_id": "student_004", "name": "Sneha Raghunathan",
        "email": "sneha.raghunathan@citchennai.net",
        "role": "student", "department": "CSE AI", "year": 2,
        "skills": ["Python", "Machine Learning", "Data Analysis", "Pandas", "SQL"],
        "interests": ["Data Science", "AI/ML", "Research"],
        "github": "github.com/sneharaghunathan", "linkedin": "linkedin.com/in/sneharaghunathan",
        "rise_score": 298,
        "rise_score_breakdown": {"achievement_quality": 80, "skill_depth": 90, "research_impact": 50, "innovation_mindset": 50, "leadership_potential": 28},
        "rise_score_meta": {"percentile": "top 20%", "reasoning": "Strong foundation with NPTEL cert and hackathon participation at Year 2.", "badge": "Rising Star", "improvement_areas": ["Build a personal ML project", "Apply for research internships"]},
        "ai_profile_summary": "Second-year CSE-AI student with solid data science fundamentals and growing achievement record.",
        "innovation_potential": "Medium-High", "suggested_roles": ["Data Scientist", "ML Engineer", "Data Analyst"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [120, 190, 250, 298]
    }

    users_db["student_005"] = {
        "user_id": "student_005", "name": "Karthik Subramaniam",
        "email": "karthik.subramaniam@citchennai.net",
        "role": "student", "department": "IT", "year": 4,
        "skills": ["Java", "Spring Boot", "MySQL", "REST APIs", "Linux"],
        "interests": ["Backend Development", "System Design", "Open Source"],
        "github": "github.com/karthiksubramaniam", "linkedin": "linkedin.com/in/karthiksubramaniam",
        "rise_score": 251,
        "rise_score_breakdown": {"achievement_quality": 70, "skill_depth": 80, "research_impact": 30, "innovation_mindset": 40, "leadership_potential": 31},
        "rise_score_meta": {"percentile": "top 30%", "reasoning": "Solid backend skills with college coding contest win.", "badge": "Builder", "improvement_areas": ["Contribute to open source", "Build a scalable side project"]},
        "ai_profile_summary": "Final-year IT student specialising in Java backend development with contest success.",
        "innovation_potential": "Medium", "suggested_roles": ["Backend Developer", "Java Engineer", "Software Developer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": [100, 165, 210, 251]
    }

    users_db["student_006"] = {
        "user_id": "student_006", "name": "Divya Lakshmi",
        "email": "divya.lakshmi@citchennai.net",
        "role": "student", "department": "Mechanical", "year": 3,
        "skills": ["AutoCAD", "SolidWorks", "3D Printing", "Product Design"],
        "interests": ["Product Design", "Startups", "Manufacturing Innovation"],
        "github": "", "linkedin": "linkedin.com/in/divyalakshmi",
        "rise_score": 189,
        "rise_score_breakdown": {"achievement_quality": 40, "skill_depth": 60, "research_impact": 30, "innovation_mindset": 40, "leadership_potential": 19},
        "rise_score_meta": {"percentile": "top 45%", "reasoning": "Startup idea submission shows entrepreneurial drive. Keep building.", "badge": "Builder", "improvement_areas": ["Get CITBIF idea formally reviewed", "Participate in national design competitions"]},
        "ai_profile_summary": "Mechanical student with product design skills and an entrepreneurial startup idea submitted to CITBIF.",
        "innovation_potential": "Medium", "suggested_roles": ["Product Design Engineer", "CAD Designer", "Startup Founder"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [80, 130, 170, 189]
    }

    users_db["student_007"] = {
        "user_id": "student_007", "name": "Rahul Annamalai",
        "email": "rahul.annamalai@citchennai.net",
        "role": "student", "department": "Civil", "year": 4,
        "skills": ["STAAD Pro", "AutoCAD", "Structural Analysis", "MATLAB"],
        "interests": ["Structural Research", "Smart Infrastructure", "Academic Research"],
        "github": "", "linkedin": "linkedin.com/in/rahulannamalai",
        "rise_score": 203,
        "rise_score_breakdown": {"achievement_quality": 70, "skill_depth": 60, "research_impact": 40, "innovation_mindset": 20, "leadership_potential": 13},
        "rise_score_meta": {"percentile": "top 40%", "reasoning": "Published research paper and smart infrastructure project are strong for Civil dept.", "badge": "Researcher", "improvement_areas": ["Present at a national conference", "Explore urban planning tech"]},
        "ai_profile_summary": "Final-year Civil student with published research and smart infrastructure project experience.",
        "innovation_potential": "Medium", "suggested_roles": ["Structural Research Engineer", "Site Engineer", "Urban Tech Consultant"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": [90, 140, 175, 203]
    }

    users_db["student_008"] = {
        "user_id": "student_008", "name": "Ananya Pillai",
        "email": "ananya.pillai@citchennai.net",
        "role": "student", "department": "Biomedical", "year": 3,
        "skills": ["MATLAB", "Python", "Medical Imaging", "Signal Processing", "Arduino"],
        "interests": ["Medical Devices", "Health Tech", "Biomedical Research"],
        "github": "github.com/ananyapillai", "linkedin": "linkedin.com/in/ananyapillai",
        "rise_score": 334,
        "rise_score_breakdown": {"achievement_quality": 120, "skill_depth": 90, "research_impact": 70, "innovation_mindset": 35, "leadership_potential": 19},
        "rise_score_meta": {"percentile": "top 12%", "reasoning": "3 verified achievements including a national symposium win makes this student a hidden gem.", "badge": "Innovator", "improvement_areas": ["Apply for biomedical research grants", "Collaborate with medical institutions"]},
        "ai_profile_summary": "Hidden gem: Biomedical student with national symposium win, research paper, and health-tech hackathon success.",
        "innovation_potential": "High", "suggested_roles": ["Medical Devices Engineer", "Biomedical Researcher", "Health-Tech Developer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [140, 210, 280, 334]
    }

    users_db["student_009"] = {
        "user_id": "student_009", "name": "Vikram Chandrasekhar",
        "email": "vikram.chandrasekhar@citchennai.net",
        "role": "student", "department": "CSE", "year": 1,
        "skills": ["C", "Python basics", "HTML"],
        "interests": ["Programming", "Gaming", "Technology"],
        "github": "", "linkedin": "",
        "rise_score": 67,
        "rise_score_breakdown": {"achievement_quality": 10, "skill_depth": 20, "research_impact": 10, "innovation_mindset": 15, "leadership_potential": 12},
        "rise_score_meta": {"percentile": "bottom 30%", "reasoning": "First year student just getting started. Huge potential ahead.", "badge": "Newcomer", "improvement_areas": ["Complete a beginner Python project", "Join a college club", "Attend your first hackathon"]},
        "ai_profile_summary": "First-year CSE student at the very start of their RISE journey with foundational programming skills.",
        "innovation_potential": "Unknown", "suggested_roles": ["Software Developer", "Full Stack Engineer", "ML Engineer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": []
    }

    users_db["student_010"] = {
        "user_id": "student_010", "name": "Meera Sundaram",
        "email": "meera.sundaram@citchennai.net",
        "role": "student", "department": "ECE", "year": 2,
        "skills": ["Basic Electronics", "Circuit Design", "Arduino basics"],
        "interests": ["IoT", "Electronics", "Robotics"],
        "github": "", "linkedin": "linkedin.com/in/meerasundaram",
        "rise_score": 112,
        "rise_score_breakdown": {"achievement_quality": 15, "skill_depth": 35, "research_impact": 20, "innovation_mindset": 25, "leadership_potential": 17},
        "rise_score_meta": {"percentile": "bottom 40%", "reasoning": "Early stage with only workshop attendance. Needs structured upskilling.", "badge": "Explorer", "improvement_areas": ["Build an Arduino IoT project", "Participate in a college-level hackathon", "Get an IoT certification"]},
        "ai_profile_summary": "Second-year ECE student with basic electronics foundation, seeking direction in IoT development.",
        "innovation_potential": "Low-Medium", "suggested_roles": ["IoT Developer", "Electronics Engineer", "Embedded Developer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [55, 90, 112]
    }

    users_db["student_011"] = {
        "user_id": "student_011", "name": "Lakshmi Narayanan",
        "email": "lakshmi.narayanan@citchennai.net",
        "role": "student", "department": "CSE AI", "year": 4,
        "skills": ["NLP", "Computer Vision", "Transformers", "HuggingFace", "FastAPI"],
        "interests": ["AI Research", "NLP", "Open Source AI"],
        "github": "github.com/lakshmi-narayanan", "linkedin": "linkedin.com/in/lakshminarayanan",
        "rise_score": 445,
        "rise_score_breakdown": {"achievement_quality": 155, "skill_depth": 130, "research_impact": 90, "innovation_mindset": 45, "leadership_potential": 25},
        "rise_score_meta": {"percentile": "top 2%", "reasoning": "Research paper + SIH win + Microsoft AI cert + viral open source project = exceptional portfolio.", "badge": "Visionary", "improvement_areas": ["Apply to top AI labs", "Mentor junior students"]},
        "ai_profile_summary": "Final-year CSE-AI powerhouse with NLP expertise, SIH win, Microsoft cert, and an open source project with 200+ GitHub stars.",
        "innovation_potential": "Very High", "suggested_roles": ["AI Research Scientist", "NLP Engineer", "ML Engineer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [200, 300, 390, 430, 445]
    }

    users_db["student_012"] = {
        "user_id": "student_012", "name": "Aakash Mohan",
        "email": "aakash.mohan@citchennai.net",
        "role": "student", "department": "IT", "year": 3,
        "skills": ["Flutter", "Firebase", "UI/UX", "Figma", "React Native"],
        "interests": ["Mobile Apps", "Startups", "Product Design"],
        "github": "github.com/aakashmohan", "linkedin": "linkedin.com/in/aakashmohan",
        "rise_score": 276,
        "rise_score_breakdown": {"achievement_quality": 90, "skill_depth": 85, "research_impact": 30, "innovation_mindset": 50, "leadership_potential": 21},
        "rise_score_meta": {"percentile": "top 25%", "reasoning": "Published app + entrepreneurship award shows real-world impact as a 3rd year.", "badge": "Builder", "improvement_areas": ["Reach 1000 Play Store downloads", "Apply to startup incubators"]},
        "ai_profile_summary": "IT entrepreneur with a published Play Store app and college entrepreneurship award.",
        "innovation_potential": "Medium-High", "suggested_roles": ["Mobile App Developer", "Product Manager", "Startup Founder"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": [110, 175, 230, 276]
    }

    users_db["student_013"] = {
        "user_id": "student_013", "name": "Pooja Ramamurthy",
        "email": "pooja.ramamurthy@citchennai.net",
        "role": "student", "department": "Mechanical", "year": 2,
        "skills": ["AutoCAD", "Engineering Drawing", "Basic MATLAB"],
        "interests": ["Manufacturing", "Design", "CAD Modelling"],
        "github": "", "linkedin": "linkedin.com/in/poojaramamurthy",
        "rise_score": 143,
        "rise_score_breakdown": {"achievement_quality": 20, "skill_depth": 50, "research_impact": 20, "innovation_mindset": 30, "leadership_potential": 23},
        "rise_score_meta": {"percentile": "bottom 35%", "reasoning": "Technical symposium participation is a start. Needs more verified achievements.", "badge": "Explorer", "improvement_areas": ["Win a design competition", "Learn SolidWorks", "Join technical clubs"]},
        "ai_profile_summary": "Second-year Mechanical student building CAD skills, beginning participation in technical events.",
        "innovation_potential": "Low-Medium", "suggested_roles": ["Manufacturing Engineer", "CAD Designer", "Production Engineer"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [70, 110, 143]
    }

    users_db["student_014"] = {
        "user_id": "student_014", "name": "Suresh Balakrishnan",
        "email": "suresh.balakrishnan@citchennai.net",
        "role": "student", "department": "Civil", "year": 3,
        "skills": ["AutoCAD", "Site Survey basics"],
        "interests": ["Construction", "Site Engineering"],
        "github": "", "linkedin": "",
        "rise_score": 88,
        "rise_score_breakdown": {"achievement_quality": 5, "skill_depth": 30, "research_impact": 10, "innovation_mindset": 25, "leadership_potential": 18},
        "rise_score_meta": {"percentile": "bottom 45%", "reasoning": "Low engagement so far. Needs guidance to participate in opportunities.", "badge": "Explorer", "improvement_areas": ["Attend a civil engineering competition", "Get STAAD-Pro certified", "Do a site internship"]},
        "ai_profile_summary": "Civil student with low engagement so far — ideal candidate for targeted mentorship and opportunity matching.",
        "innovation_potential": "Low", "suggested_roles": ["Site Engineer", "Field Engineer", "Construction Supervisor"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "male", "avatar_generated_at": None,
        "score_history": []
    }

    users_db["student_015"] = {
        "user_id": "student_015", "name": "Nithya Krishnan",
        "email": "nithya.krishnan@citchennai.net",
        "role": "student", "department": "CSE", "year": 4,
        "skills": ["Python", "Django", "AWS", "DevOps", "Docker", "Kubernetes"],
        "interests": ["DevOps", "Cloud", "Startups", "Entrepreneurship"],
        "github": "github.com/nithyakrishnan", "linkedin": "linkedin.com/in/nithyakrishnan",
        "rise_score": 389,
        "rise_score_breakdown": {"achievement_quality": 120, "skill_depth": 110, "research_impact": 50, "innovation_mindset": 70, "leadership_potential": 39},
        "rise_score_meta": {"percentile": "top 7%", "reasoning": "Registered startup + hackathon runner-up + AWS cert makes a rare entrepreneurial profile.", "badge": "Innovator", "improvement_areas": ["Scale startup to first paying customers", "Speak at a tech event"]},
        "ai_profile_summary": "Final-year CSE entrepreneur with a registered startup, national hackathon runner-up, and AWS certification.",
        "innovation_potential": "Very High", "suggested_roles": ["DevOps Engineer", "Cloud Architect", "Startup Founder"],
        "career_roadmap": None, "created_at": datetime.utcnow().isoformat(),
        "avatar_config": None, "gender": "female", "avatar_generated_at": None,
        "score_history": [160, 250, 330, 389]
    }

    achievements_db.update({
        # student_001 – Arjun Krishnamurthy
        "ach_001_1": {"achievement_id": "ach_001_1", "student_id": "student_001", "title": "IEEE Conference Paper — ML Optimisation", "type": "research", "description": "Co-authored and published a paper at IEEE on neural network optimisation techniques.", "date": "2024-10-12", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_001_2": {"achievement_id": "ach_001_2", "student_id": "student_001", "title": "Winner — National ML Hackathon 2024", "type": "hackathon", "description": "First place at a national-level machine learning hackathon with 500+ participants.", "date": "2024-08-20", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_001_3": {"achievement_id": "ach_001_3", "student_id": "student_001", "title": "Google ML Bootcamp Certificate", "type": "certification", "description": "Completed Google's intensive Machine Learning Bootcamp with distinction.", "date": "2024-06-15", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_002 – Priya Venkatesh
        "ach_002_1": {"achievement_id": "ach_002_1", "student_id": "student_002", "title": "SIH 2024 Finalist", "type": "hackathon", "description": "Reached the national finals of Smart India Hackathon 2024.", "date": "2024-09-10", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_002_2": {"achievement_id": "ach_002_2", "student_id": "student_002", "title": "Open Source Contributor — Major React Library", "type": "opensource", "description": "Merged 5 PRs into a popular open source React component library.", "date": "2024-07-05", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_002_3": {"achievement_id": "ach_002_3", "student_id": "student_002", "title": "Internship — Zoho Corp (Full Stack)", "type": "internship", "description": "6-month internship at Zoho working on internal SaaS tooling.", "date": "2024-12-01", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_003 – Mohammed Farhan
        "ach_003_1": {"achievement_id": "ach_003_1", "student_id": "student_003", "title": "Patent Filed — Energy-Efficient FPGA Architecture", "type": "patent", "description": "Filed patent for a novel low-power FPGA architecture design.", "date": "2024-11-01", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_003_2": {"achievement_id": "ach_003_2", "student_id": "student_003", "title": "State-Level Best Project Award — ECE Symposium", "type": "award", "description": "Won best project award at state-level ECE symposium for IoT home automation.", "date": "2024-04-18", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_004 – Sneha Raghunathan
        "ach_004_1": {"achievement_id": "ach_004_1", "student_id": "student_004", "title": "Hackathon Participation — DataHack 2024", "type": "hackathon", "description": "Participated in national-level data science hackathon at Year 2.", "date": "2024-08-30", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_004_2": {"achievement_id": "ach_004_2", "student_id": "student_004", "title": "NPTEL Certificate — Machine Learning", "type": "certification", "description": "Completed NPTEL 12-week Machine Learning course with distinction.", "date": "2024-05-20", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_005 – Karthik Subramaniam
        "ach_005_1": {"achievement_id": "ach_005_1", "student_id": "student_005", "title": "Winner — College Coding Contest (CodeIT 2024)", "type": "competition", "description": "First place at college-level competitive programming contest.", "date": "2024-03-15", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_006 – Divya Lakshmi
        "ach_006_1": {"achievement_id": "ach_006_1", "student_id": "student_006", "title": "Startup Idea Submitted to CITBIF", "type": "startup", "description": "Submitted a product design startup idea to CIT Business Incubation Forum.", "date": "2025-01-10", "verified": False, "created_at": datetime.utcnow().isoformat()},

        # student_007 – Rahul Annamalai
        "ach_007_1": {"achievement_id": "ach_007_1", "student_id": "student_007", "title": "Research Paper Published — Smart Infrastructure", "type": "research", "description": "Published paper on sensor-based smart infrastructure monitoring in a national journal.", "date": "2024-09-25", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_007_2": {"achievement_id": "ach_007_2", "student_id": "student_007", "title": "Smart Infrastructure Campus Project", "type": "project", "description": "Led a team to deploy IoT-based structural health monitoring on campus buildings.", "date": "2024-11-15", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_008 – Ananya Pillai
        "ach_008_1": {"achievement_id": "ach_008_1", "student_id": "student_008", "title": "Winner — National Biomedical Symposium 2024", "type": "award", "description": "First prize at the National Biomedical Engineering Symposium for ECG signal analysis project.", "date": "2024-10-05", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_008_2": {"achievement_id": "ach_008_2", "student_id": "student_008", "title": "Research Paper — ECG Anomaly Detection using Deep Learning", "type": "research", "description": "Co-authored and submitted research paper to a biomedical IEEE journal.", "date": "2024-12-10", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_008_3": {"achievement_id": "ach_008_3", "student_id": "student_008", "title": "Health-Tech Hackathon — Top 5", "type": "hackathon", "description": "Reached top 5 at national health-tech hackathon with a wearable monitoring solution.", "date": "2024-07-22", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_010 – Meera Sundaram (pending)
        "ach_010_1": {"achievement_id": "ach_010_1", "student_id": "student_010", "title": "IoT Workshop Attendance — TechFest 2025", "type": "workshop", "description": "Attended 2-day IoT hands-on workshop at college TechFest.", "date": "2025-01-20", "verified": False, "created_at": datetime.utcnow().isoformat()},

        # student_011 – Lakshmi Narayanan
        "ach_011_1": {"achievement_id": "ach_011_1", "student_id": "student_011", "title": "Research Paper — Multilingual NLP Transformers", "type": "research", "description": "Published research on multilingual transformer fine-tuning at an international NLP workshop.", "date": "2024-11-05", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_011_2": {"achievement_id": "ach_011_2", "student_id": "student_011", "title": "Winner — Smart India Hackathon 2024", "type": "hackathon", "description": "Won SIH 2024 with an AI-powered sign language accessibility platform.", "date": "2024-09-12", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_011_3": {"achievement_id": "ach_011_3", "student_id": "student_011", "title": "Microsoft AI-900 & AI-102 Certificates", "type": "certification", "description": "Earned both Azure AI Fundamentals and AI Engineer certifications.", "date": "2024-06-20", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_011_4": {"achievement_id": "ach_011_4", "student_id": "student_011", "title": "Open Source NLP Toolkit — 200+ GitHub Stars", "type": "opensource", "description": "Built and maintained an open source NLP preprocessing toolkit with 200+ GitHub stars.", "date": "2024-08-01", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_012 – Aakash Mohan
        "ach_012_1": {"achievement_id": "ach_012_1", "student_id": "student_012", "title": "App Published on Google Play Store", "type": "project", "description": "Developed and launched a student productivity Flutter app on Google Play Store.", "date": "2024-10-18", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_012_2": {"achievement_id": "ach_012_2", "student_id": "student_012", "title": "College Entrepreneurship Award 2024", "type": "award", "description": "Recognised by college entrepreneurship cell for best student startup.", "date": "2024-12-05", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # student_013 – Pooja Ramamurthy (pending)
        "ach_013_1": {"achievement_id": "ach_013_1", "student_id": "student_013", "title": "Technical Symposium Participation", "type": "event", "description": "Presented a CAD model project at the departmental technical symposium.", "date": "2025-02-10", "verified": False, "created_at": datetime.utcnow().isoformat()},

        # student_015 – Nithya Krishnan
        "ach_015_1": {"achievement_id": "ach_015_1", "student_id": "student_015", "title": "Startup Registered — CloudOps.ai", "type": "startup", "description": "Officially registered CloudOps.ai, a DevOps automation startup.", "date": "2024-11-20", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_015_2": {"achievement_id": "ach_015_2", "student_id": "student_015", "title": "Runner-up — National Hackathon (DevOps Track)", "type": "hackathon", "description": "Second place at national-level hackathon in the DevOps/Cloud track.", "date": "2024-07-15", "verified": True, "created_at": datetime.utcnow().isoformat()},
        "ach_015_3": {"achievement_id": "ach_015_3", "student_id": "student_015", "title": "AWS Solutions Architect Associate Certificate", "type": "certification", "description": "Earned AWS SAA certification demonstrating cloud architecture proficiency.", "date": "2024-05-10", "verified": True, "created_at": datetime.utcnow().isoformat()},

        # original demo student achievements
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
