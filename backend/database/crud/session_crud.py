from sqlalchemy.orm import Session
from database.models.session import SessionModel  # This is your model
from database.schemas.session_schema import SessionBase  # This is your schema

def create_session(db: Session, session_data: SessionBase):
    new_session = SessionModel(
        session_id = session_data.session_id,
        student_id = session_data.student_id,
        started_at = session_data.started_at,
        status = session_data.status,
        end_at = session_data.end_at
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session