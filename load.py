import csv
import datetime
import pytz

from app import models
from app.database import SessionLocal, engine

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

with open('McQO_WAV_2023.csv', 'r') as f:
    csv_reader = csv.DictReader(f, skipinitialspace=True)

    # Skips the second header line
    next(csv_reader)

    for row in csv_reader:
        t = datetime.datetime.strptime(row['time'], '%d-%b-%Y %H:%M:%S')
        utc = pytz.utc
        t = utc.localize(t)

        db_record = models.Record(
            timestamp=t,
            wave_height=row['WVHT'],
            mean_wave_direction=row['MWD'],
            dominant_wave_period=row['DPD'],
        )
        db.add(db_record)

    db.commit()

db.close()
