from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Evaluation(Base):
    __tablename__ = 'evaluations'

    evaluation_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    remark = Column(String, nullable=True)

    session = relationship("SessionModel", back_populates="evaluation")
