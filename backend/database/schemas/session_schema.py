from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base shared schema
class SessionBase(BaseModel):
    session_id : str
    student_id: int
    started_at: Optional[datetime] = None
    status: Optional[str] = None
    end_at: Optional[datetime] = None

    class Config:
        orm_mode = True
