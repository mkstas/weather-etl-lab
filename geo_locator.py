import requests

def get_geodata():
    response = requests.get("https://ipinfo.io/json")
    return response.json()
