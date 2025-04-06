from sqlalchemy.orm import Session
from database.model import Student

def get_student_by_email_and_id(db: Session, email: str, rollno: str):
    return db.query(Student).filter(
        Student.email == email,
        Student.rollno == rollno
    ).first()
    
def get_student_by_credentials(db: Session, name: str, email: str, rollno: str):
    return db.query(Student).filter(
        Student.name == name,
        Student.email == email,
        Student.rollno == rollno
    ).first()

def create_student(db: Session, name: str, email: str, rollno: str):
    new_student = Student(name=name, email=email, rollno=rollno)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
