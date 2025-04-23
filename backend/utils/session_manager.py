import uuid
import os
import json
from datetime import datetime
from fastapi import HTTPException

SESSION_DIR = "data/sessions"
SESSION_FILE_PATH = os.path.join(SESSION_DIR, "session_store.json")


def _load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def _save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def create_session(student_data, student_id: int):
    sessions = _load_json(SESSION_FILE_PATH)
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "studentId": student_id,
        "login_time": datetime.now().isoformat()
    }

    _save_json(sessions, SESSION_FILE_PATH)

    # Create individual session file with full data
    create_current_session(session_id, student_id, student_data)

    return session_id


def create_current_session(session_id, student_id, student_data):
    session_data = {
        "session_id": session_id,
        "student_id": student_id,
        "name": student_data.name,
        "email": student_data.email,
        "roll_number": student_data.roll_number,
        "login_time": datetime.now().isoformat(),
        "selected_topics": {}  # e.g., {"Unit Name 1": ["Topic A", "Topic B"]}
    }

    session_file_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    _save_json(session_data, session_file_path)


def get_student_from_session(session_id):
    sessions = _load_json(SESSION_FILE_PATH)
    if session_id in sessions:
        return sessions[session_id]
    raise HTTPException(status_code=401, detail="Invalid or expired session")

