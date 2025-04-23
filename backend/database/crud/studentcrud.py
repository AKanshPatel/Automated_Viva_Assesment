from sqlalchemy.orm import Session
from database.models.student import Student
import json

def get_student_id_by_rollno(db: Session, rollno: str):
    student = db.query(Student).filter(Student.roll_number == rollno).first()
    if student:
        return student.student_id
    return None

def get_student_by_credentials(db: Session, name: str, email: str, rollno: str):
    return db.query(Student).filter(
        Student.name == name,
        Student.email == email,
        Student.roll_number == rollno
    ).first()

def get_all_students(db: Session):
    return db.query(Student).all()

def add_students_to_db(db: Session, students: list):
    db.add_all(students)
    db.commit()
    for student in students:
        db.refresh(student)
    return students

# Validation function to check if a student already exists
def is_student_exists(db: Session, roll_number: str, email: str) -> bool:
    return db.query(Student).filter(
        (Student.roll_number == roll_number) |
        (Student.email == email)
    ).first() is not None

# Main function to add students if they do not already exist
def add_students_from_json_if_not_exists(db: Session, json_path: str):
    with open("database/students.json", 'r') as f:
        data = json.load(f)

    added_students = []
    for student_data in data:
        if not is_student_exists(db, student_data["roll_number"], student_data["email"]):
            student = Student(
                name=student_data["name"],
                email=student_data["email"],
                roll_number=student_data["roll_number"]
            )
            added_students.append(student)

    # Now add all the new students using the existing function
    if added_students:
        add_students_to_db(db, added_students)

    return added_students
