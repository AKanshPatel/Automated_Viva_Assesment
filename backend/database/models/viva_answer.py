from sqlalchemy import Column, String, Integer
from database.connection import Base, engine

class VivaAnswer(Base):
    __tablename__ = "VivaAnswer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, index=True)
    session_id = Column(String(50), index=True)
    question_no = Column(String(50), index=True)
    question_text = Column(String(255), nullable=False)
    answer_text = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(String(255), nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)