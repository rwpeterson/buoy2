from datetime import datetime
from pydantic import BaseModel


class RecordBase(BaseModel):
    timestamp: datetime
    wave_height: float
    mean_wave_direction: float
    dominant_wave_period: float

class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True

class RecordCreate(RecordBase):
    pass
