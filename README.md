# ⚡ CIT RISE — Research & Innovation Student Ecosystem

> AI-powered campus innovation platform for Chennai Institute of Technology.
> Built with FastAPI + React + Gemini AI + CareerNav AI.

---

## Quick Start

### Requirements
- **Python 3.13.x** — https://www.python.org/downloads/
- **Node.js 18+** — https://nodejs.org/

### Step 1 — Gemini API Key (free, 2 min)
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key (starts with `AIza...`)

### Step 2 — Backend
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file:
echo GEMINI_API_KEY=your_key_here > .env

uvicorn main:app --reload
```
Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Step 3 — Frontend (new terminal)
```bash
cd frontend
npm install
npm start
```
Frontend runs at: http://localhost:3000

---

## Demo Login
| Role | User ID |
|------|---------|
| Student | `student_demo` |
| Admin | `admin_001` |

---

## Features
- AI profile generation from PDF resume upload
- CIT RISE Innovation Score (AI-calculated, not rule-based)
- Personalized career roadmap (CareerNav AI)
- Live GitHub repo analysis
- Live LeetCode stats + DSA study plan
- AI chat assistant
- Admin talent intelligence dashboard
- Achievement tracking + manual verification
- Mentor matching by skill
- Opportunity broadcasting

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18 |
| Backend | Python 3.13, FastAPI |
| AI | Google Gemini 1.5 Flash |
| External APIs | GitHub Public API, LeetCode GraphQL |
| PDF Parsing | pdfplumber |
