from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base  # assumes you have a Base from SQLAlchemy

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)

    sessions = relationship("SessionModel", back_populates="student")
