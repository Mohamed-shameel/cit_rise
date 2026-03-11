from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from config.store import messages_db, users_db, mentors_db

router = APIRouter()


class MessageReq(BaseModel):
    student_id: str
    mentor_id: str
    text: str
    sender: str  # "student" or "mentor"


def _conv_key(student_id: str, mentor_id: str) -> str:
    return f"{student_id}__{mentor_id}"


@router.post("/message")
async def send_message(req: MessageReq):
    if req.sender == "student" and req.student_id not in users_db:
        raise HTTPException(404, "Student not found")
    if req.mentor_id not in mentors_db:
        raise HTTPException(404, "Mentor not found")
    if not req.text.strip():
        raise HTTPException(400, "Message cannot be empty")

    key = _conv_key(req.student_id, req.mentor_id)
    if key not in messages_db:
        messages_db[key] = []

    msg = {
        "sender": req.sender,
        "text": req.text.strip(),
        "timestamp": datetime.utcnow().isoformat(),
    }
    messages_db[key].append(msg)

    # First message from student earns XP
    student_msgs = [m for m in messages_db[key] if m["sender"] == "student"]
    if len(student_msgs) == 1 and req.sender == "student":
        student = users_db.get(req.student_id)
        if student:
            student["xp"] = student.get("xp", 0) + 5

    return {"success": True, "message": msg, "conversation_key": key}


@router.get("/conversation/{student_id}/{mentor_id}")
async def get_conversation(student_id: str, mentor_id: str):
    key = _conv_key(student_id, mentor_id)
    messages = messages_db.get(key, [])
    mentor = mentors_db.get(mentor_id, {})
    return {
        "student_id": student_id,
        "mentor_id": mentor_id,
        "mentor_name": mentor.get("name", "Mentor"),
        "messages": messages,
        "total": len(messages),
    }


@router.get("/my-conversations/{student_id}")
async def get_student_conversations(student_id: str):
    convs = []
    for key, msgs in messages_db.items():
        if key.startswith(f"{student_id}__"):
            mentor_id = key.split("__")[1]
            mentor = mentors_db.get(mentor_id, {})
            if msgs:
                convs.append({
                    "mentor_id": mentor_id,
                    "mentor_name": mentor.get("name", "Unknown"),
                    "mentor_company": mentor.get("company", ""),
                    "last_message": msgs[-1],
                    "total_messages": len(msgs),
                })
    return {"student_id": student_id, "conversations": convs}


@router.get("/mentor-inbox/{mentor_id}")
async def mentor_inbox(mentor_id: str):
    inbox = []
    for key, msgs in messages_db.items():
        if key.endswith(f"__{mentor_id}"):
            student_id = key.split("__")[0]
            student = users_db.get(student_id, {})
            if msgs:
                inbox.append({
                    "student_id": student_id,
                    "student_name": student.get("name", "Unknown"),
                    "department": student.get("department", ""),
                    "last_message": msgs[-1],
                    "total_messages": len(msgs),
                    "unread": True,
                })
    return {"mentor_id": mentor_id, "conversations": inbox}
