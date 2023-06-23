from sqlalchemy.orm import Session

from . import models, schemas

def get_record(db: Session, id: int):
    return db.query(models.Record).get(id)

def get_records(db: Session):
    return db.query(models.Record).all()

def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
