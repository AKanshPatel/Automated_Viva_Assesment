from pydantic import BaseModel, EmailStr

class StudentRead(BaseModel):
    student_id: int
    name: str
    email: EmailStr
    roll_number: str

    class Config:
        orm_mode = True  # Important! Allows reading from SQLAlchemy models
