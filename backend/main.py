from fastapi import FastAPI , HTTPException, Depends 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime
import os
import json
import uuid
from database.connection import get_db
from database.crud import studentcrud 
from utils import session_manager 


# from database import SessionLocal
from database.crud import studentcrud
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentLogin(BaseModel):
    # student_id : int
    name: str
    email: str
    roll_number: str

class TopicSelection(BaseModel):
    sessionId: str
    selected_topics: Dict[str, List[str]]  # e.g., {"Unit Name 1": ["Topic A", "Topic B"]}


@app.post("/login")
def login(student_data: StudentLogin, db: Session = Depends(get_db)):
    print(f"Received student data: {student_data}")
    # 1. Verify student credentials
    db_student = studentcrud.get_student_by_credentials(
        db=db,
        name=student_data.name,
        email=student_data.email,
        rollno=student_data.roll_number
    )
    if db_student:
        # 2. Get student_id
        student_id = db_student.student_id
        # 3. Create session using updated session_manager
        session_id = session_manager.create_session(student_data, student_id)
        return {
            "message": "Login successful",
            "session_id": session_id
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    

# GET /question-bank
@app.get("/question-bank")
def get_question_bank():
    file_path = os.path.join("data", "question_bank.json")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Question bank file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding question bank")
    

@app.post("/save-topics")
def save_topics(topicsData: TopicSelection): 
    session_id = topicsData.sessionId
    selected_topics = topicsData.selected_topics
    session_file_path = f"data/sessions/{session_id}.json"

    # Check if session file exists
    if not os.path.exists(session_file_path):
        raise HTTPException(status_code=404, detail="Session file not found.")

    try:
        with open(session_file_path, 'r') as file:
            session_data = json.load(file)

        # Overwrite with new selected_topics
        session_data["selected_topics"] = selected_topics

        with open(session_file_path, 'w') as file:
            json.dump(session_data, file, indent=4)

        return {"message": "Selected topics saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session file: {str(e)}")
