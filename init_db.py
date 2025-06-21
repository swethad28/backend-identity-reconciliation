# init_db.py

from database import engine
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)
