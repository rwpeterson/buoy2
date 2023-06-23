from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Blocks(directory='templates')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("home/index.html", {'request': request})

@app.get('/clicked')
def salute(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('home/index.html', {'request': request, 'salutation': 'Goodnight, Moon!' }, block_name = 'message')

@app.get("/records/", response_model=list[schemas.Record])
def get_records(db: Session = Depends(get_db)):
    records = crud.get_records(db)
    return records

@app.get('/records/{id}', response_model=schemas.Record)
def get_record(id: int, db: Session = Depends(get_db)):
    record = crud.get_record(db, id=id)
    return record

@app.post('/records/', response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    return crud.create_record(db, record=record)
