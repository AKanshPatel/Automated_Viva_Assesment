# import os
# import json
# from fastapi import FastAPI, HTTPException, Query
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Dict, List, Optional


# class AnswerResult(BaseModel):
#     question_no: int
#     question_text: str
#     answer_text: Optional[str] = None
#     score: float
#     max_score: float


# class ExamResult(BaseModel):
#     student_name: str
#     roll_number: str
#     student_id: str  # This field is defined as a string
#     session_id: str
#     answers: List[AnswerResult]
#     total_score: float
#     max_score: float


# def get_results(session_id: str = Query(..., description="The session ID of the student")):
#     session_file_path = f"data/sessions/{session_id}.json"
#     answer_file_path = f"data/answers/{session_id}_full.json"

#     if not os.path.exists(session_file_path):
#         raise HTTPException(status_code=404, detail="Session file not found")

#     try:
#         with open(session_file_path, "r", encoding="utf-8") as session_file:
#             session_data = json.load(session_file)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to read session file: {str(e)}")

#     # student_id = session_data.get("student_id")  #  <-- Potential Issue
#     student_id = str(session_data.get("student_id"))  # Ensure student_id is a string.
#     session_id = session_data.get("session_id")

#     # Fetch additional student info from database (optional) or mock for now
#     # Here assuming the session file includes everything needed
#     student_name = session_data.get("name", "Unknown Student")  # Optional fields
#     roll_number = session_data.get("roll_number", "N/A")

#     # Step 2: Load answer file
#     if not os.path.exists(answer_file_path):
#         raise HTTPException(status_code=404, detail="Answer file not found")

#     try:
#         with open(answer_file_path, "r", encoding="utf-8") as answer_file:
#             answer_data = json.load(answer_file)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to read answer file: {str(e)}")

#     answers_raw = answer_data.get("answers", [])

#     # Build AnswerResult list and calculate total scores
#     answers = []
#     total_score = 0
#     max_score = 0

#     for answer in answers_raw:
#         score = answer.get("score", 0)
#         max_s = 10  # Default max_score
#         total_score += score
#         max_score += max_s

#         answers.append(
#             AnswerResult(
#                 question_no=answer.get("question_no", 0),
#                 question_text=answer.get("question_text", "Unknown question"),
#                 answer_text=answer.get("answer_text", ""),
#                 score=score,
#                 max_score=max_s,
#             )
#         )

#     result = ExamResult(
#         student_name=student_name,
#         roll_number=roll_number,
#         student_id=student_id,
#         session_id=session_id,
#         answers=answers,
#         total_score=total_score,
#         max_score=max_score,
#     )

#     print(result)  # For debugging purposes
#     return result # Added return statement so that the function returns the result.


# if __name__ == "__main__":
#     # You would typically get the session_id from the user's request in a FastAPI application.
#     # For this example, we'll use a hardcoded session ID.  Make sure this session ID
#     # exists in your data/sessions directory.  I've added a return statement to the
#     # get_results function, and am calling it here, and printing the result.
#     session_id_to_test = "6fb2ac1f-74df-40af-a61e-92669d800b71" # Replace with a valid session ID
#     try:
#         result = get_results(session_id_to_test)
#         print(result)
#     except HTTPException as e:
#         print(f"Error: {e.detail}")

import json
import os
from typing import List

def fetch_question_texts(session_id: str) -> List[str]:
    file_path = f"data/questions/{session_id}.json"

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No question file found for session ID: {session_id}")

    # Read and parse the file
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            questions_data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {file_path}")

    # Extract question_texts
    question_texts = [item["question_text"] for item in questions_data if "question_text" in item]
    print(question_texts)
    return question_texts

fetch_question_texts("8f22b869-02e1-4880-a5ed-93cd8fe47a02")