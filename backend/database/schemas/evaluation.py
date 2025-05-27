from pydantic import BaseModel
from typing import Optional


# Base schema
class EvaluationBase(BaseModel):
    session_id: int
    total_score: Optional[float] = None
    overall_feedback: Optional[str] = None


# For creating evaluation
class EvaluationCreate(EvaluationBase):
    pass


# For returning evaluation
class EvaluationOut(EvaluationBase):
    evaluation_id: int

    class Config:
        orm_mode = True
