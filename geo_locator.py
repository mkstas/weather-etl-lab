import requests

def get_geodata():
    response = requests.get("https://ipinfo.io/json")
    print(response.json())
    return response.json()
