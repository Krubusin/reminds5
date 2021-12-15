import datetime
from pydantic import BaseModel, Field

class BookingCreate(BaseModel):
    subject_id: int
    subject_num: int
    end_date: datetime.date


class Booking(BookingCreate):
    booking_id: int

    class Config:
        orm_mode = True

class SubjectCreate(BaseModel):
    subjectname: str = Field(max_length=20)

class Subject(SubjectCreate):
    subject_id: int

    class Config:
        orm_mode = True

