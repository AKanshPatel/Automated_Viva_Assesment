# Project Overview!

## Folder Structure

```plaintext
backend/
│
├── data/
│   ├── question_bank.json            # JSON file containing question bank
│   ├── students_data                 # Students info that needs to be feed in DB 
│   └── sessions/                     # folder for storing session data 
│         ├── session_store.json      # Stores session data for all the previous sessions
│         ├── {session_id}.json       # stores the info of student, session_id and selected_topics 
│
│
├── database/  
│   ├── crud/
│   │     ├── __init__.py                    
│   │     └── studentcrud.py         # CRUD operations for Studnets Table
│   │
│   ├── schemas/
│   │     ├── __init__.py 
│   │     └── student_schema.py      # Schema 
│   │
│   ├── __init__.py
│   ├── connection.py                # Connenct to database 
│   ├── models/ 
│   │      └── student.py            # Student Table     
│   └── load_students.py             # utility script for loading students         
│
├── models/                          # folder for models (content not listed)
│
├── requirements.txt                 # project dependencies
└── viva.db                          # database file
