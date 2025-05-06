# viva_answer_crud.py
from sqlalchemy.orm import Session
from models.viva_answer import Student  # This is your model
from schemas.viva_answer_schema import VivaAnswerSchema  # This is your schema

def add_viva_answer(db: Session, answer: VivaAnswerSchema):
    db_answer = Student(
        student_id=answer.student_id,
        session_id=answer.session_id,
        question_no=answer.question_no,
        question_text=answer.question_text,
        answer_text=answer.answer_text,
        score=answer.score,
        feedback=answer.feedback
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_score_feedback_by_question(db: Session, session_id: str, question_no: int):
    db_answer = db.query(Student).filter_by(session_id=session_id, question_no=question_no).first()
    
    if not db_answer:
        return None
    
    # Returning only score, feedback, and question_text
    return {
        "score": db_answer.score,
        "feedback": db_answer.feedback,
        "question_text": db_answer.question_text
    }


def get_all_answers_for_session(db: Session, session_id: str):
    # Query to get all records for the given session_id
    db_answers = db.query(Student).filter(Student.session_id == session_id).all()
    
    if not db_answers:
        return None
    
    # Returning a list of questions, answers, scores, and feedback
    return [
        {
            "question_text": answer.question_text,
            "answer_text": answer.answer_text,
            "score": answer.score,
            "feedback": answer.feedback
        }
        for answer in db_answers
    ]

def get_all_students(db: Session):
    db_students = db.query(Student).all()  # Get all rows from the Student table
    return db_students

