from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.connection import Base, engine  # Adjust the path based on your project

class Student(Base):
    __tablename__ = "VivaAnswer"
    
    student_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(50), unique=True, index=True)
    question_no = Column(String(50), unique=True, index=True)
    question_text = Column(String(255), nullable=False) 
    answer_text = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False) 
    feedback = Column(String(255), nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)