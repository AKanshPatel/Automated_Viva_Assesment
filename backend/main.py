from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os
import json

# Import DB session and model logic
from database import SessionLocal
from crud import student as crud_student

app = FastAPI()

# Allow CORS for local frontend (e.g., Next.js at http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request body model
class StudentLogin(BaseModel):
    name: str
    email: str
    studentId: str

# Login endpoint
@app.post("/login")
def login(student_data: StudentLogin, db: Session = Depends(get_db)):
    print(f"Received student: {student_data}")
    
    # Check DB for student with matching credentials
    db_student = crud_student.get_student_by_credentials(
        db=db,
        name=student_data.name,
        email=student_data.email,
        rollno=student_data.studentId
    )

    if db_student:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

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
        raise HTTPException(status_code=500, detail="Error decoding JSON")