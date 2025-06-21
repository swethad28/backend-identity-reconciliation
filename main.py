# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Contact
import schemas  # We’ll create this next
import logic    # We’ll create this after schemas

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify_contact(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    try:
        return logic.process_contact(payload, db)
    except Exception as e:
        raise HTTPException(status_code=418, detail="Temporal trace disrupted 🌀")
