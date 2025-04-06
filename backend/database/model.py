from sqlalchemy import Column, String, Integer, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Student(Base):
    __tablename__ = "students"
    
    rollno = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    viva_answers = relationship("VivaAnswer", back_populates="student")
    performance = relationship("Performance", back_populates="student", uselist=False)

class VivaAnswer(Base):
    __tablename__ = "viva_answers"

    id = Column(Integer, primary_key=True, index=True)
    rollno = Column(String, ForeignKey("students.rollno"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    score = Column(Integer)

    student = relationship("Student", back_populates="viva_answers")

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    rollno = Column(String, ForeignKey("students.rollno"), nullable=False, unique=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    score = Column(Float)

    student = relationship("Student", back_populates="performance")
