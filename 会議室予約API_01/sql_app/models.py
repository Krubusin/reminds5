from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .datebase import Base

class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True, index=True)
    subjectname = Column(String, unique=True, index=True)



class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='SET NULL'), nullable=False)
    subject_num = Column(Integer)
    end_date = Column(DateTime, nullable=False)
