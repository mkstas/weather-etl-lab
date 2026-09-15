from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    forecast_date = Column(Date, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    description = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
