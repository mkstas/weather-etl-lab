from sqlalchemy import create_engine
from db_models import Base
from geo_locator import get_geodata
from weather_client import get_weather_forecoast
from dotenv import load_dotenv

import os

load_dotenv()

weather_forecoast_api_key = os.environ.get("WEATHER_FORECAST_API_KEY")

engine = create_engine("sqlite:///weather_lab.db")

Base.metadata.create_all(engine)

geodata = get_geodata()
get_weather_forecoast(geodata['city'], appid=weather_forecoast_api_key)
