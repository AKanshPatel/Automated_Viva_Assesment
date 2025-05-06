from sqlalchemy.orm import Session
from database.connection import SessionLocal  # adjust the import path based on your project
from crud.viva_answer_crud import get_all_students

def test_get_all_viva_answers():
    # Create a database session
    db: Session = SessionLocal()

    try:
        # Fetch all records
        all_data = get_all_students(db)

        if not all_data:
            print("No records found in the VivaAnswer table.")
            return

        # Print each record
        print("\nAll Records in VivaAnswer Table:\n")
        for record in all_data:
            print(f"Student ID   : {record.student_id}")
            print(f"Session ID   : {record.session_id}")
            print(f"Question No  : {record.question_no}")
            print(f"Question     : {record.question_text}")
            print(f"Answer       : {record.answer_text}")
            print(f"Score        : {record.score}")
            print(f"Feedback     : {record.feedback}")
            print("-" * 50)
    finally:
        # Always close the DB session
        db.close()

if __name__ == "__main__":
    test_get_all_viva_answers()
