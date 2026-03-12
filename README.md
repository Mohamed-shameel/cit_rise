# ⚡ CIT RISE — Research & Innovation Student Ecosystem

> An AI-powered campus innovation ecosystem that centralizes student achievements, career intelligence, and mentor connections — built for Chennai Institute of Technology.

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-4285F4?style=flat-square)
![CareerNav](https://img.shields.io/badge/Integrated-CareerNav%20AI-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 Problem

College innovation exists in silos. Clubs use Excel sheets. Students store certificates locally. Alumni are only reachable via LinkedIn. The institution cannot answer: *"Who are our top innovators? Which startups are active? How is innovation growing?"*

**CIT RISE solves this** — one centralized platform that manages the entire campus innovation ecosystem.

---

## 🎯 What CIT RISE Does

| Feature | Type |
|--------|------|
| AI profile generation from resume | 🤖 Gemini AI |
| RISE Innovation Score (CIBIL-like) | 🤖 Gemini AI |
| Personalized career roadmap | 🤖 Gemini AI |
| GitHub repo analysis + skill detection | 🤖 CareerNav × GitHub API |
| LeetCode stats + DSA study plan | 🤖 CareerNav × LeetCode API |
| Admin talent intelligence dashboard | 🤖 Gemini AI |
| AI chat assistant (EduBot) | 🤖 Gemini AI |
| Achievement tracking + verification | 👤 Manual (Admin) |
| Mentor/alumni matching | ⚡ Skill-based |
| Opportunity broadcasting | 👤 Manual (Admin) |

**AI Coverage: ~75%** — AI handles intelligence, humans handle governance.

---

## 🏗 Architecture

```
React Frontend
      ↓  REST API
FastAPI Backend
      ↓
In-Memory Store (demo) → Firestore (production)
      ↓
Gemini 1.5 Flash API  +  GitHub Public API  +  LeetCode GraphQL API
```

---

## 🔬 CareerNav AI Integration

CIT RISE integrates **CareerNav AI** (Team Helios) for developer intelligence:

- **GitHub Analysis** — fetches real repos via GitHub public API, Gemini classifies domain, skill level, career readiness, open source score
- **LeetCode Analysis** — fetches real stats via LeetCode GraphQL, Gemini generates personalized DSA study plan and interview readiness assessment
- Skills detected from GitHub are automatically merged into the student's CIT RISE profile and trigger an AI score recalculation

---

## 🧩 Modules

1. **Innovation Profile System** — AI-generated student profiles from resume text
2. **RISE Score Engine** — AI-calculated innovation score with reasoning (not rule-based)
3. **Career Roadmap** — Personalized AI roadmap with milestones, skill gaps, salary outlook
4. **CareerNav Intelligence** — GitHub + LeetCode live analysis
5. **Mentor & Alumni Engagement** — Skill-based mentor matching
6. **Event & Achievement Tracker** — Upload achievements, admin verification
7. **Opportunity Broadcasting** — Internships, competitions, research openings
8. **Admin Dashboard** — Analytics, AI talent insights, NAAC/NIRF ready

---

## 🚀 Running Locally

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Backend
**Note:** Open a dedicated terminal for the backend. If using Windows, activating the Python `venv` might conflict with global npm commands later, so always keep your backend and frontend in separate tabs!

```bash
cd backend
# Activate your virtual environment (Windows)
.\venv\Scripts\activate
pip install -r requirements.txt

# Create .env file if you haven't already
echo "GEMINI_API_KEY=your_key_here" > .env
# Start server
uvicorn main:app --reload
# API docs at http://localhost:8000/docs
```

### Frontend
**Note:** Open a *new, separate terminal* for the frontend (do NOT activate the Python `venv` here).

```bash
cd frontend
npm install
npm start
# App at http://localhost:3000
```

*Troubleshooting:* If you recently installed Node.js but `npm start` tells you "npm is not recognized", you may need to completely restart VS Code or your computer to reload your system PATH. Alternatively, you can temporarily inject it into your current PowerShell session:
```powershell
$env:Path += ";C:\Program Files\nodejs"
npm start
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/ai-profile-from-resume` | AI generates profile from resume |
| `POST` | `/ai/recalculate-score` | AI calculates CIT RISE score |
| `POST` | `/ai/career-roadmap` | AI generates career roadmap |
| `GET`  | `/ai/admin-insights` | AI talent intelligence |
| `POST` | `/ai/chat` | AI assistant chat |
| `POST` | `/careernav/github` | GitHub repo analysis |
| `POST` | `/careernav/leetcode` | LeetCode stats + study plan |
| `POST` | `/achievements/add` | Add achievement |
| `PUT`  | `/achievements/{id}/verify` | Admin: verify achievement |
| `GET`  | `/admin/dashboard` | Admin overview |
| `GET`  | `/mentors/recommend/{id}` | Mentor recommendations |

Full interactive docs at `/docs` when running locally.

---

## 🖥 Demo Flow

```
1. Login as student  →  student@spark.in / spark123
2. AI Profile Gen    →  paste resume → Gemini builds profile + score
3. CareerNav         →  enter GitHub username → live repo analysis
4. CareerNav         →  enter LeetCode username → DSA study plan
5. Career Roadmap    →  AI generates personalized roadmap
6. Login as admin    →  admin@spark.in / admin123
7. Admin Dashboard   →  verify achievements, AI talent insights
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, CSS-in-JS |
| Backend | Python, FastAPI |
| AI | Google Gemini 2.5 Flash (or whichever model your API key supports) |
| External APIs | GitHub Public API, LeetCode GraphQL |
| Database | In-memory (demo) → Firebase Firestore (production) |
| Deployment | Render (backend), Vercel (frontend) |

### Why this stack?
- **FastAPI:** Extremely high performance for AI data processing and asynchronous tasks, enabling real-time generation of roadmaps and resume parsing without blocking the main workflow.
- **React 18:** Enables a highly responsive, single-page application experience with rapid state updates for complex dashboards.
- **Gemini 2.5 Flash:** Offers the optimal balance of speed, cost, and expansive context windows required to ingest entire student resumes and generate massive JSON intelligence reports instantly.
- **External GraphQL/REST APIs:** Directly interfacing with GitHub and LeetCode guarantees that the "Innovation Profile" relies on cryptographically verifiable proof-of-work rather than student self-reporting.

---

## 👥 Team

**Team CIT RISE** — Chennai Institute of Technology

- Built for the college innovation ecosystem
- CareerNav AI integration by Team Helios

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
