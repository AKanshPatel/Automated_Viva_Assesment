from database.crud.studentcrud import add_students_from_json_if_not_exists
from database.connection import get_db
import json
import os

# db = get_db()
# Load students from JSON file
with open("database/students.json", "r") as file:
    student_list = json.load(file)
print(student_list)

db = next(get_db())
add_students_from_json_if_not_exists(db, "database/students.json")


