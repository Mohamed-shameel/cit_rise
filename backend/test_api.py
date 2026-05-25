import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import json
import io
import pypdfium2


# Import the app
from main import app
from config.store import users_db, achievements_db, mentors_db, opportunities_db, user_opportunities, ideas_db

class TestCitRiseAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Clean state / seed if needed for tests
        pass

    def test_root_and_health(self):
        """Test health check and root endpoints"""
        r_root = self.client.get("/")
        self.assertEqual(r_root.status_code, 200)
        self.assertIn("platform", r_root.json())

        r_health = self.client.get("/health")
        self.assertEqual(r_health.status_code, 200)
        self.assertEqual(r_health.json(), {"status": "ok"})

    def test_users_crud(self):
        """Test user creation, listing, details and update"""
        # 1. Create a user
        user_data = {
            "name": "Test Student",
            "email": "test@citchennai.net",
            "department": "ECE",
            "year": 2,
            "skills": ["Python", "C++"],
            "interests": ["Robotics"],
            "github": "test-git",
            "linkedin": "test-li"
        }
        res = self.client.post("/users/create", json=user_data)
        self.assertEqual(res.status_code, 200)
        user_id = res.json()["user_id"]
        self.assertIsNotNone(user_id)

        # 2. Get the created user
        res_get = self.client.get(f"/users/{user_id}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["name"], "Test Student")

        # 3. List all users
        res_list = self.client.get("/users/")
        self.assertEqual(res_list.status_code, 200)
        self.assertGreaterEqual(res_list.json()["total"], 1)

        # 4. Update the user
        update_data = {
            "skills": ["Python", "C++", "ROS"],
            "interests": ["Robotics", "IoT"]
        }
        res_up = self.client.put(f"/users/{user_id}/update", json=update_data)
        self.assertEqual(res_up.status_code, 200)
        self.assertIn("ROS", res_up.json()["user"]["skills"])

    @patch("services.ai_service.call_llama", new_callable=AsyncMock)
    def test_users_ai_profile_from_resume(self, mock_llama):
        """Test generating student profile from a PDF resume upload (mocked AI)"""
        # Setup mock return for profile extraction
        mock_llama.side_effect = [
            # First call inside generate_student_profile
            json.dumps({
                "name": "Resume Candidate",
                "department": "CSE AI",
                "year": 3,
                "skills": ["Python", "ML", "FastAPI"],
                "interests": ["AI", "Startups"],
                "strengths": ["Quick Learner"],
                "profile_summary": "Highly motivated ML enthusiast.",
                "innovation_potential": "High",
                "suggested_roles": ["ML Engineer"]
            }),
            # Second call inside calculate_rise_score
            json.dumps({
                "total_score": 240,
                "breakdown": {"achievement_quality": 80, "skill_depth": 70, "research_impact": 50, "innovation_mindset": 30, "leadership_potential": 10},
                "percentile": "top 10%",
                "score_reasoning": "Strong academic record and ML focus.",
                "improvement_areas": ["Open source contributions"],
                "badge": "Innovator"
            })
        ]

        # Simulate PDF file upload using dummy text
        pdf_data = io.BytesIO(b"%PDF-1.4 ... dummy content ...")
        # Mock pypdfium2 PdfDocument
        mock_pdf = MagicMock()
        mock_pdf.__len__.return_value = 1
        
        mock_page = MagicMock()
        mock_textpage = MagicMock()
        mock_textpage.get_text_range.return_value = "Candidate Name: Resume Candidate\nSkills: Python, ML, FastAPI\nDept: CSE AI"
        mock_page.get_textpage.return_value = mock_textpage
        mock_pdf.__getitem__.return_value = mock_page
        
        with patch("pypdfium2.PdfDocument", return_value=mock_pdf):
            files = {"resume_file": ("resume.pdf", pdf_data, "application/pdf")}
            data = {"email": "resume@citchennai.net", "github_username": "candidate-git"}
            res = self.client.post("/users/ai-profile-from-resume", files=files, data=data)
            
            self.assertEqual(res.status_code, 200)
            json_res = res.json()
            self.assertEqual(json_res["profile"]["name"], "Resume Candidate")
            self.assertEqual(json_res["profile"]["rise_score"], 240)



    @patch("services.ai_service.call_llama", new_callable=AsyncMock)
    def test_achievements_flow(self, mock_llama):
        """Test adding, verifying, and rejecting achievements"""
        mock_llama.return_value = json.dumps({
            "total_score": 150,
            "breakdown": {"achievement_quality": 50, "skill_depth": 40},
            "percentile": "top 30%",
            "score_reasoning": "Recalculated with new achievement.",
            "improvement_areas": [],
            "badge": "Explorer"
        })

        # 1. Add achievement
        ach_data = {
            "student_id": "student_demo",
            "title": "Smart India Hackathon 2024 Winner",
            "type": "hackathon",
            "description": "Won first prize in AI track",
            "date": "2024-09-15",
            "certificate_url": "cert-sih-2024"
        }
        res = self.client.post("/achievements/add", json=ach_data)
        self.assertEqual(res.status_code, 200)
        ach_id = res.json()["achievement"]["achievement_id"]
        self.assertIsNotNone(ach_id)

        # 2. Get achievements for student
        res_get = self.client.get("/achievements/student_demo")
        self.assertEqual(res_get.status_code, 200)
        self.assertGreaterEqual(len(res_get.json()["achievements"]), 1)

        # 3. Verify achievement
        res_ver = self.client.put(f"/achievements/{ach_id}/verify")
        self.assertEqual(res_ver.status_code, 200)
        self.assertTrue(res_ver.json()["achievement"]["verified"])

        # 4. Reject/Flag achievement
        res_rej = self.client.delete(f"/achievements/{ach_id}/reject?reason=Expired")
        self.assertEqual(res_rej.status_code, 200)
        self.assertFalse(res_rej.json()["achievement"]["verified"])
        self.assertTrue(res_rej.json()["achievement"]["rejected"])

    @patch("services.ai_service.call_llama", new_callable=AsyncMock)
    def test_ai_roadmap_and_chat(self, mock_llama):
        """Test AI personalized career roadmap and AI chat assistant"""
        # Mock career roadmap
        mock_llama.return_value = json.dumps({
            "primary_career_path": "Data Scientist",
            "current_level": "Intermediate",
            "time_to_job_ready": "6 months",
            "immediate_actions": [{"action": "Build kaggle project", "why": "Show ML skills", "timeline": "2 weeks"}],
            "skill_gaps": [{"skill": "Statistics", "priority": "High", "resource": "Khan Academy"}],
            "milestones": [{"month": 1, "goal": "Statistics complete", "outcome": "Ready"}],
            "recommended_projects": ["Predictive housing ML model"],
            "salary_outlook": {"fresher": "8 LPA", "3_years": "18 LPA"},
            "motivational_note": "You have a solid base, keep pushing."
        })
        res_rm = self.client.post("/ai/career-roadmap", json={"student_id": "student_demo"})
        self.assertEqual(res_rm.status_code, 200)
        self.assertEqual(res_rm.json()["roadmap"]["primary_career_path"], "Data Scientist")

        # Mock AI Chat response
        mock_llama.return_value = "Keep focusing on solving problems on Leetcode and developing high quality projects."
        res_chat = self.client.post("/ai/chat", json={"student_id": "student_demo", "question": "What should I do next?"})
        self.assertEqual(res_chat.status_code, 200)
        self.assertIn("Leetcode", res_chat.json()["answer"])

    def test_opportunities_management(self):
        """Test opportunity operations (listing, registering, updating status, admin CRUD)"""
        # 1. List all opportunities
        res_list = self.client.get("/opportunities/")
        self.assertEqual(res_list.status_code, 200)
        self.assertGreaterEqual(res_list.json()["total"], 1)

        # 2. Admin creates a new custom opportunity
        opp_data = {
            "title": "Robotics Research Internship",
            "description": "Work in our state of the art embedded systems lab.",
            "domain": ["Robotics", "IoT"],
            "type": "research",
            "company": "CIT Robotics Lab",
            "location": "Chennai",
            "source_url": "https://citchennai.edu/robotics-internship",
            "deadline": "2026-06-01",
            "salary_range": "Rs 8,000/month",
            "duration": "2 months"
        }
        res_create = self.client.post("/opportunities/admin/create", json=opp_data)
        self.assertEqual(res_create.status_code, 200)
        opp_id = res_create.json()["opportunity_id"]
        self.assertIsNotNone(opp_id)

        # 3. User registers for opportunity
        res_reg = self.client.post(f"/opportunities/{opp_id}/register", json={"user_id": "student_demo"})
        self.assertEqual(res_reg.status_code, 200)
        self.assertEqual(res_reg.json()["message"], "Registered successfully")

        # Test registering an invalid user
        res_reg_err = self.client.post(f"/opportunities/{opp_id}/register", json={"user_id": "invalid_user"})
        self.assertEqual(res_reg_err.status_code, 404)

        # 4. Fetch registered opportunities for user
        res_user_opps = self.client.get("/opportunities/user/student_demo")
        self.assertEqual(res_user_opps.status_code, 200)
        self.assertGreaterEqual(res_user_opps.json()["total"], 1)

        # 5. Update opportunity status to ongoing
        res_status = self.client.put(f"/opportunities/{opp_id}/user/student_demo/status", json={"status": "ongoing"})
        self.assertEqual(res_status.status_code, 200)
        self.assertEqual(res_status.json()["registration"]["status"], "ongoing")

        # 6. Admin verifies opportunity
        res_ver = self.client.put(f"/opportunities/admin/{opp_id}/verify")
        self.assertEqual(res_ver.status_code, 200)
        self.assertTrue(res_ver.json()["opportunity"]["verified"])

    @patch("services.ai_service.call_llama", new_callable=AsyncMock)
    def test_ideas_submission_and_admin_review(self, mock_llama):
        """Test student ideas system (details, comments, admin reviews, CSV export/import)"""
        # 1. Get student's ideas
        res_ideas = self.client.get("/ideas/my-ideas?user_id=student_demo")
        self.assertEqual(res_ideas.status_code, 200)
        self.assertGreaterEqual(res_ideas.json()["total"], 1)

        # 2. Get single idea details
        res_detail = self.client.get("/ideas/idea-sample-1?user_id=student_demo")
        self.assertEqual(res_detail.status_code, 200)
        self.assertEqual(res_detail.json()["idea"]["title"], "AI-Powered Tutoring Platform")

        # 3. Admin review an idea
        review_data = {
            "status": "selected",
            "admin_comment": "Excellent work Shameel! Recalculating score.",
            "mentor_assignment": "m1"
        }
        res_review = self.client.post("/ideas/idea-sample-1/review?admin_user_id=admin_001", json=review_data)
        self.assertEqual(res_review.status_code, 200)
        self.assertEqual(res_review.json()["status"], "selected")
        self.assertEqual(res_review.json()["rise_score_boost"], 40)

        # 4. Admin add custom comment
        comment_data = {"comment": "Looking forward to the presentation!"}
        res_comment = self.client.post("/ideas/idea-sample-1/comment?admin_user_id=admin_001", json=comment_data)
        self.assertEqual(res_comment.status_code, 200)
        self.assertEqual(res_comment.json()["comment_added"]["comment"], "Looking forward to the presentation!")

        # 5. Export ideas as CSV
        res_export = self.client.get("/ideas/admin/export-csv")
        self.assertEqual(res_export.status_code, 200)
        self.assertIn("csv_data", res_export.json())

        # 6. Admin stats endpoint
        res_stats = self.client.get("/ideas/admin/stats")
        self.assertEqual(res_stats.status_code, 200)
        self.assertGreaterEqual(res_stats.json()["total_ideas"], 1)

        # 7. Import ideas CSV (mocked)
        mock_llama.return_value = json.dumps({
            "category": "FinTech",
            "feasibility_score": 88,
            "mentor_field_suggestions": ["ML"],
            "feasibility_reasoning": "High impact idea.",
            "implementation_complexity": "Medium",
            "potential_impact": "High",
            "suggested_first_steps": ["Step 1"]
        })
        csv_data = "Timestamp,Email Address,Your Name,Idea Title,Detailed Explanation\n5/25/2026 12:00:00,arjun@cit.in,Arjun K,Blockchain Banking,Secure decentralized transactions.\n"
        csv_file = io.BytesIO(csv_data.encode('utf-8'))
        files = {"file": ("ideas_import.csv", csv_file, "text/csv")}
        res_import = self.client.post("/ideas/admin/import-csv?admin_user_id=admin_001", files=files)
        self.assertEqual(res_import.status_code, 200)
        self.assertIn("Successfully imported and analyzed", res_import.json()["message"])

    def test_mentors_recommendations(self):
        """Test listing mentors and fetching skills-based matches"""
        # 1. List mentors
        res_list = self.client.get("/mentors/")
        self.assertEqual(res_list.status_code, 200)
        self.assertGreaterEqual(res_list.json()["total"], 1)

        # 2. Get mentor recommendations for student
        res_recs = self.client.get("/mentors/recommend/student_demo")
        self.assertEqual(res_recs.status_code, 200)
        self.assertGreaterEqual(len(res_recs.json()["recommended_mentors"]), 1)

    def test_admin_dashboard(self):
        """Test admin overview dashboard stats"""
        res = self.client.get("/admin/dashboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn("stats", res.json())
        self.assertGreaterEqual(res.json()["stats"]["total_students"], 1)

if __name__ == "__main__":
    unittest.main()
