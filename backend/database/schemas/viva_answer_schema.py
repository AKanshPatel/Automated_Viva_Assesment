from pydantic import BaseModel
from typing import Optional

class VivaAnswerSchema(BaseModel):
    student_id: int
    session_id: str
    question_no: str
    question_text: str
    answer_text: str
    score: int
    feedback: str

    class Config:
        orm_mode = True

# Optional: for returning data that includes the auto-generated `id`
class VivaAnswerOutSchema(VivaAnswerSchema):
    id: int
