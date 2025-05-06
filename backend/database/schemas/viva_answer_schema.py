from pydantic import BaseModel

class viva_answer_schema(BaseModel):
    student_id: int
    session_id: str
    question_no: int
    question_text: str
    answer_text: str
    score: int
    feedback: str

    class Config:
        orm_mode = True  # Important! Allows reading from SQLAlchemy models