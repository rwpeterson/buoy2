from sqlalchemy import Column, Double, Integer, String
from sqlalchemy_utc import UtcDateTime
from .database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(UtcDateTime)
    wave_height = Column(Double)
    mean_wave_direction = Column(Double)
    dominant_wave_period = Column(Double)
