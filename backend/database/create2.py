from sqlalchemy import create_engine
from database.connection import Base, engine

from database.models import viva_answer  # replace with actual import

engine = create_engine('sqlite:///viva.db')  # path to your DB file
Base.metadata.create_all(engine)