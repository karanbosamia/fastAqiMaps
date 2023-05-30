from fastapi import FastAPI
import enum
from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Enum
from sqlalchemy.orm import relationship


class PollutantEnum(enum.Enum):
    co_2 = 'co2'
    o_3 = 'o3'
    pm_10 = 'pm10'
    pm_25 = 'pm25'


class AirQualityData(Base):
    __tablename__ = "air_quality_data"

    id = Column(Integer, primary_key=True, index=True)
    aqi = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    write_date = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


class PollutantForecastData(Base):
    __tablename__ = "pollutant_forecast_data"

    Id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    pollutant = Column(Date)
    record_date = Column(Date)
    day_maximum = Column(Float)
    day_minimum = Column(Float)

