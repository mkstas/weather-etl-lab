import logging
import os

from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from db_models import Base, WeatherForecast
from geo_locator import get_geodata
from weather_client import get_weather_forecast, aggregate_forecast
from exporter import export_to_markdown

load_dotenv()

weather_forecoast_api_key = os.environ.get("WEATHER_FORECAST_API_KEY")

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s]: %(message)s")

logger = logging.getLogger(__name__)

engine = create_engine("sqlite:///weather_lab.db")

Base.metadata.create_all(engine)


def main():
    geodata = get_geodata()
    city = geodata["city"]

    logger.info(f"Automatically determined location: {city}")

    try:
        data = get_weather_forecast(city, weather_forecoast_api_key)
        daily = aggregate_forecast(data)
    except Exception as ex:
        logging.error("Unable to retrieve the forecast: %s", ex)
        return

    date_now = datetime.now(timezone.utc).replace(tzinfo=None)

    if not daily:
        logging.warning("No forecast data to save")
        export_to_markdown(engine, city)
        return

    values = [
        {
            "city": city,
            "forecast_date": day["forecast_date"],
            "temp_min": day["temp_min"],
            "temp_max": day["temp_max"],
            "humidity": day["humidity"],
            "wind_speed": day["wind_speed"],
            "description": day["description"],
            "created_at": date_now,
        }
        for day in daily
    ]

    with Session(engine) as session:
        stmt = insert(WeatherForecast).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=["city", "forecast_date"])
        session.execute(stmt)
        session.commit()

    logging.info(f"Weather forecast for {city} saved")
    export_to_markdown(engine, city)


if __name__ == "__main__":
    main()
