# view_students.py

from sqlalchemy.orm import Session
from database.connection import engine
from database.crud.studentcrud import get_all_students,is_student_exists ,get_student_id_by_rollno  # Adjust the import according to your structure

# Create a new session
# with Session(engine) as session:
#     students = get_all_students(session)

#     if not students:
#         print("No students found in the database.")
#     else:
#         print("Students in the database:")
#         for student in students:
#             print(f"Name: {student.name}, Email: {student.email}, Roll Number: {student.roll_number}")

with Session(engine) as session:
    students = get_all_students(session)
    print(students)
    if not students:
        print("No students found in the database.")
    else:
        print("Students in the database:")
        for student in students:
            print(f"Student ID: {student.student_id}, Name: {student.name}, Email: {student.email}, Roll Number: {student.roll_number}")
            student_id = get_student_id_by_rollno(session, student.roll_number)
            print(f"Student ID by Roll Number: {student_id}")
            print(f"Is Student Exists: {is_student_exists(session, student.roll_number, student.email)}")