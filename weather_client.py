import requests

def get_weather_forecoast(city, appid):
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}&units=metric&lang=ru")
    print(response.json())
