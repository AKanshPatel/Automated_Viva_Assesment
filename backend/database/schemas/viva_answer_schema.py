from pydantic import BaseModel
from typing import Optional


# Base Schema: shared across create and update
class VivaAnswerBase(BaseModel):
    question_no: Optional[int]
    question_text: str
    answer_text: str
    score: Optional[float] = None
    feedback: Optional[str] = None
    session_id: int


# For Creating a new VivaAnswer
class VivaAnswerCreate(VivaAnswerBase):
    pass


# For Reading a VivaAnswer (i.e., API response)
class VivaAnswer(VivaAnswerBase):
    response_id: int

    class Config:
        orm_mode = True
