from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.connection import Base, engine  # Adjust the path based on your project

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    roll_number = Column(String, nullable=False, unique=True)

    # Relationships (you should define the other side in respective models)
    viva_answers = relationship("VivaAnswer", back_populates="student")
    # performance = relationship("Performance", back_populates="student", uselist=False)

# Function to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
