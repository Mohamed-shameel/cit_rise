import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, achievements, ai, admin, opportunities, mentors, careernav, ideas, avatar, chat, notifications

app = FastAPI(title="CIT RISE API", version="1.0.0",
    description="Research & Innovation Student Ecosystem — CIT Chennai")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(users.router,        prefix="/users",       tags=["Users"])
app.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
app.include_router(ai.router,           prefix="/ai",          tags=["AI"])
app.include_router(admin.router,        prefix="/admin",       tags=["Admin"])
app.include_router(opportunities.router,prefix="/opportunities",tags=["Opportunities"])
app.include_router(mentors.router,      prefix="/mentors",     tags=["Mentors"])
app.include_router(careernav.router,    prefix="/careernav",   tags=["CareerNav AI"])
app.include_router(ideas.router,        prefix="/ideas",       tags=["Ideas"])
app.include_router(avatar.router,       prefix="/avatar",       tags=["Avatar"])

app.include_router(chat.router,         prefix="/chat",         tags=["MentorChat"])
app.include_router(notifications.router,prefix="/notifications", tags=["Notifications"])

API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/")
def root():
    return {"platform":"CIT RISE","status":"running","docs":"/docs"}

@app.get("/health")
def health():
    return {"status":"ok"}
