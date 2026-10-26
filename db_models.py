from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class WeatherForecast(Base):
    __tablename__ = "weather_forecast"
    __table_args__ = (UniqueConstraint("city", "forecast_date", name="uq_city_forecast_date"),)

    id = Column(Integer, primary_key=True)
    city = Column(String)
    forecast_date = Column(Date)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    created_at = Column(DateTime)
