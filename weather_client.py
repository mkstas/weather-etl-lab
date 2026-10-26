import requests

from datetime import datetime, timedelta, timezone


def get_weather_forecast(city, appid):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}&units=metric&lang=ru",
            timeout=30,
        )
    except requests.exceptions.Timeout:
        raise Exception("Timeout (30s) on OpenWeatherMap API request")
    except requests.exceptions.ConnectionError:
        raise Exception("No connection to the OpenWeatherMap API")
    except requests.exceptions.RequestException as ex:
        raise Exception(f"Network error during API request: {ex}")

    if response.status_code == 401:
        raise Exception("Invalid OpenWeatherMap API key")
    if response.status_code == 404:
        raise Exception(f"City {city} not found")
    if response.status_code == 429:
        raise Exception("OpenWeatherMap API request limit exceeded")

    return response.json()


def aggregate_forecast(data):
    timezone_offset = data["city"]["timezone"]
    buckets = {}

    for entry in data["list"]:
        local_dt = datetime.fromtimestamp(entry["dt"], tz=timezone.utc) + timedelta(seconds=timezone_offset)
        buckets.setdefault(local_dt.date(), []).append(
            {
                "temp_min": entry["main"]["temp_min"],
                "temp_max": entry["main"]["temp_max"],
                "humidity": entry["main"]["humidity"],
                "wind_speed": entry["wind"]["speed"],
                "description": entry["weather"][0]["description"],
                "_local_hour": local_dt.hour
            }
        )

    today = datetime.now(timezone.utc).date() + timedelta(seconds=timezone_offset)
    selected_days = sorted(d for d in buckets if today <= d < today + timedelta(days=4))

    aggregated = []

    for day in selected_days:
        entries = buckets[day]
        midday = min(entries, key=lambda e: abs(e["_local_hour"] - 12))

        aggregated.append(
            {
                "forecast_date": day,
                "temp_min": min(e["temp_min"] for e in entries),
                "temp_max": max(e["temp_max"] for e in entries),
                "humidity": round(sum(e["humidity"] for e in entries) / len(entries)),
                "wind_speed": max(e["wind_speed"] for e in entries),
                "description": midday["description"]
            }
        )

    return aggregated
