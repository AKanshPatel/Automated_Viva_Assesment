from sqlalchemy.orm import Session
from database.models.session import Session_model  # This is your model
from database.schemas.session import SessionBase  # This is your schema

def create_session(db: Session, session_data: SessionBase):
    new_session = Session_model(
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