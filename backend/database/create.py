# backend/create_tables.py
from database.connection import Base, engine
from database.models import student  # import all models here

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")
