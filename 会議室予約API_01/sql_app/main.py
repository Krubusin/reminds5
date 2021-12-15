from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .datebase import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)




app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# async def index():
    # return {"message": "Success"}

# Read
@app.get("/subjects", response_model=List[schemas.Subject])
async def read_subjects(skip: int= 0, limit: int =100, db: Session = Depends(get_db)):
    subjects = crud.get_subjects(db,skip=skip,limit=limit)
    return subjects


@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int= 0, limit: int =100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db,skip=skip,limit=limit)
    return bookings



# Creat
@app.post("/subjects",response_model=schemas.Subject)
async def create_subject(subject: schemas.SubjectCreate,db: Session = Depends(get_db)):
    return crud.create_subject(db=db, subject=subject)


@app.post("/bookings",response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate,db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)

