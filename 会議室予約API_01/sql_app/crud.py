from sqlalchemy.orm import Session
from . import models, schemas

# 教科一覧取得
def get_subjects(db: Session, skip: int = 0,limit: int =100):
    return db.query(models.Subject).offset(skip).limit(limit).all()



# 予約一覧取得
def get_bookings(db: Session, skip: int = 0,limit: int =100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

# ユーザー登録
def create_subject(db: Session, subject: schemas.Subject):
    db_subject = models.Subject(subjectname=subject.subjectname)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject



# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    db_booking = models.Booking(
        subject_id=booking.subject_id,
        subject_num=booking.subject_num,
        end_date=booking.end_date

    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking