from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime
import os
import json
from database.connection import get_db
from utils import session_manager 
from app.question_manager import QuestionManager
from fastapi.staticfiles import StaticFiles
from fastapi import File, UploadFile, Form 
from app.evaluation_manager import EvaluationManager

# from database import crud
from database.crud import studentcrud, session_crud
from database.schemas import session_schema 
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audio_dir = os.path.join("data", "audio")
os.makedirs(audio_dir, exist_ok=True)  # Ensure the directory exists
app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")

class StudentLogin(BaseModel):
    # student_id : int
    name: str
    email: str
    roll_number: str

class TopicSelection(BaseModel):
    sessionId: str
    selected_topics: Dict[str, List[str]]  # e.g., {"Unit Name 1": ["Topic A", "Topic B"]}

class QuestionResponse(BaseModel):
    questionText: str
    audioUrl: str
    totalQuestions: int

class AnswerResult(BaseModel):
    question_no: int
    question_text: str
    answer_text: Optional[str] = None
    score: float
    max_score: float

class ExamResult(BaseModel):
    student_name: str
    roll_number: str
    student_id: str
    session_id: str
    answers: List[AnswerResult]
    total_score: float
    max_score: float

# Define constants for file paths
DATA_SESSIONS_FOLDER = "data/sessions"
DATA_ANSWERS_FOLDER = "data/answers"


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
        
        # 4 Add the session data to the session table
        started_at = datetime.now()
        # Format as string: "DD/MM/YYYY, HH:MM"
        formatted_datetime = started_at.strftime("%d/%m/%Y, %H:%M")
        session_data = session_schema.SessionBase(
            session_id = session_id,
            student_id = student_id,
            started_at = datetime.now(),
            status = "active",
            end_at = None    
        )
        session_crud.create_session(
            db = db,
            session_data = session_data
        )
        
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

@app.get("/questions")
def get_question(session_id: str = Query(..., description="The ID of the exam session"),
                 question_index: int = Query(..., description="The index of the question to retrieve")):
    """
    Retrieves a specific question and its audio URL for a given session and index.
    """
    # question_index = question_index + 1  # Adjusting to 1-based index for user-friendliness
    print(f"Session ID: {session_id}, Question Index: {question_index}")
    try: 
        question_manager = QuestionManager(session_id, question_index)
        question_text, audio_url = question_manager.run()
        print(f"http://localhost:8000/audio/{session_id}_question_{question_index}_audio.mp3")
        return QuestionResponse(
            questionText = question_text,
            audioUrl = f"http://localhost:8000/audio/{session_id}_question_{question_index}_audio.mp3",
            totalQuestions = 3  # Replace with dynamic count if available
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/api/rephrase")
def get_rephrased_question(
    session_id: str = Query(..., description="The ID of the exam session"),
    question_index: int = Query(..., description="The index of the question to retrieve")
):   
    try:
        question_manager = QuestionManager(session_id, question_index)
        intent_text = question_manager.handle_intent_rephrase()
        print(intent_text)
        return {"rephrased": intent_text} 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    
@app.get("/api/hint")
def get_hint_question(
    session_id: str = Query(..., description="The ID of the exam session"),
    question_index: int = Query(..., description="The index of the question to retrieve")
):
    try: 
        question_manager = QuestionManager(session_id, question_index)
        intent_text = question_manager.handle_intent_hint()
        return {"hint": intent_text}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        
@app.get("/api/context") 
def get_context_question(
    session_id: str = Query(..., description="The ID of the exam session"),
    question_index: int = Query(..., description="The index of the question to retrieve")
):
    try: 
        question_manager = QuestionManager(session_id, question_index)
        intent_text = question_manager.handle_intent_context()
        return {"context": intent_text}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/submit")
def submit_answer(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    question_index: str = Form(...),
    question_text: str = Form(...)
):
    """
    Endpoint to receive and process audio answers along with related information.
    
    
    - Save the answer file
    - Transcribe the audio 
    - Evaluate the answer
    - Save the session_id, question text, answer text, question index, score, feedback
    
    """
    try:
        # Convert question_index to int for proper handling
        q_index = int(question_index)
        
        # Create the filename for the answer audio
        filename = f"{session_id}_answer_{q_index}.mp3"
        file_path = os.path.join(audio_dir, filename)
        
        
        
        # Log the received data
        print(f"Processing submission:")
        print(f"- Session ID: {session_id}")
        print(f"- Question Index: {q_index}")
        print(f"- Question Text: {question_text}")
        print(f"- Audio Filename: {audio.filename}")
        print(f"- Saving to: {file_path}")
        
        # Save the audio file
        with open(file_path, "wb") as f:
            contents = audio.file.read()
            f.write(contents)
        
        evaluation_manager = EvaluationManager(session_id, q_index, question_text)
        evaluation_manager.run()
        
        total_questions = 5
        is_last_question = q_index >= total_questions - 1
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Answer submitted successfully",
                "file_path": f"/audio/{filename}",
                "isLastQuestion": is_last_question
            }
        )
    
    except Exception as e:
        print(f"Error processing submission: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to process submission: {str(e)}"}
        )

@app.get("/results", response_model=ExamResult)
def get_results(session_id: str = Query(..., description="The session ID of the student")):
    session_file_path = f"data/sessions/{session_id}.json"
    answer_file_path = f"data/answers/{session_id}_full.json"

    if not os.path.exists(session_file_path):
        raise HTTPException(status_code=404, detail="Session file not found")

    try:
        with open(session_file_path, "r", encoding="utf-8") as session_file:
            session_data = json.load(session_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read session file: {str(e)}")

    # student_id = session_data.get("student_id")  #  <-- Potential Issue
    student_id = str(session_data.get("student_id"))  # Ensure student_id is a string.
    session_id = session_data.get("session_id")

    # Fetch additional student info from database (optional) or mock for now
    # Here assuming the session file includes everything needed
    student_name = session_data.get("name", "Unknown Student")  # Optional fields
    roll_number = session_data.get("roll_number", "N/A")

    # Step 2: Load answer file
    if not os.path.exists(answer_file_path):
        raise HTTPException(status_code=404, detail="Answer file not found")

    try:
        with open(answer_file_path, "r", encoding="utf-8") as answer_file:
            answer_data = json.load(answer_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read answer file: {str(e)}")

    answers_raw = answer_data.get("answers", [])

    # Build AnswerResult list and calculate total scores
    answers = []
    total_score = 0
    max_score = 0

    for answer in answers_raw:
        score = answer.get("score", 0)
        max_s = 10  # Default max_score
        total_score += score
        max_score += max_s

        answers.append(
            AnswerResult(
                question_no=answer.get("question_no", 0),
                question_text=answer.get("question_text", "Unknown question"),
                answer_text=answer.get("answer_text", ""),
                score=score,
                max_score=max_s,
            )
        )

    result = ExamResult(
        student_name=student_name,
        roll_number=roll_number,
        student_id=student_id,
        session_id=session_id,
        answers=answers,
        total_score=total_score,
        max_score=max_score,
    )
    return result