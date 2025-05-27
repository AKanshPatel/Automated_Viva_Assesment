from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class VivaAnswer(Base):
    __tablename__ = 'viva_answers'

    response_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    question_no = Column(Integer)
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(String, nullable=True)

    session = relationship("Session", back_populates="viva_answers")
