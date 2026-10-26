import os
import requests

from dotenv import load_dotenv


load_dotenv()

fallback_city = os.environ.get("GEO_API_FALLBACK_CITY")


def get_geodata():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
        data = response.json()
        return data["city"]
    except:
        return fallback_city
