# seed_students_from_json.py

import json
from database import SessionLocal
from crud.student import create_student, get_student_by_email_and_id

# Load students from JSON file
with open("students.json", "r") as file:
    student_list = json.load(file)

db = SessionLocal()
added = 0
skipped = 0

for data in student_list:
    existing_student = get_student_by_email_and_id(db, data["email"], data["rollno"])
    if existing_student:
        print(f"Skipped duplicate: {data['name']} ({data['email']})")
        skipped += 1
        continue

    create_student(db, name=data["name"], email=data["email"], rollno=data["rollno"])
    print(f"Added: {data['name']} ({data['email']})")
    added += 1

db.close()
print(f"\nSummary: {added} added, {skipped} skipped.")
