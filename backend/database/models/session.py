from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class SessionModel(Base):
    __tablename__ = 'sessions'

    session_id = Column(String, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    started_at = Column(String, nullable=False)  # Use DateTime if you plan to store timestamp
    status = Column(String, nullable = False)
    end_at = Column(String)
    student = relationship("Student", back_populates="sessions")
    viva_answers = relationship("VivaAnswer", back_populates="session")
    evaluation = relationship("Evaluation", back_populates="session", uselist=False)
