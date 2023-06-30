from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date

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

@app.get('/records', response_class=HTMLResponse)
def browse_records(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
):
    page_size = 10
    offset = (page - 1) * page_size
    records = db.query(models.Record).order_by(models.Record.timestamp.desc()).offset(offset).limit(page_size)
    context = {'request': request, 'records': records, 'page': page}
    return templates.TemplateResponse('home/records.html', context, block_name='table_swap')

@app.get('/daily', response_class=HTMLResponse)
def daily_summary(request: Request, db: Session = Depends(get_db)):
    agg_data = db.query(
        func.DATE(models.Record.timestamp).label('date'),
        func.avg(models.Record.wave_height).label('average_wave_height'),
        func.max(models.Record.wave_height).label('max_wave_height'),
    ).group_by(func.DATE(models.Record.timestamp)).order_by("date").all()
    day_summaries = [{'date': day[0], 'average_wave_height': day[1], 'max_wave_height': day[2]} for day in agg_data]
    context = {'request': request, 'day_summaries': day_summaries}
    return templates.TemplateResponse('home/summary.html', context)

@app.get("/api/records/", response_model=list[schemas.Record])
def get_records(db: Session = Depends(get_db)):
    records = crud.get_records(db)
    return records

@app.get('/api/records/{id}', response_model=schemas.Record)
def get_record(id: int, db: Session = Depends(get_db)):
    record = crud.get_record(db, id=id)
    return record

@app.post('/api/records/', response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    return crud.create_record(db, record=record)
