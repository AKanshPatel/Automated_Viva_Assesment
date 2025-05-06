

from sqlalchemy.orm import Session
from database.models.viva_answer import VivaAnswer  # Import your model

def get_all_students(db: Session):
    db_students = db.query(VivaAnswer).all()
    return db_students

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the engine and session
engine = create_engine("sqlite:///your_db_name.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

# Create a session and use the function
db = SessionLocal()
students = get_all_students(db)

# Print student data
for student in students:
    print(f"{student.student_id} - {student.question_text} - Score: {student.score}")