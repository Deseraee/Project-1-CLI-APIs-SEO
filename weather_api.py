import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENUV_API_KEY = os.getenv("OPENUV_API_KEY")
AQICN_API_KEY = os.getenv("AQICN_API_KEY")


def get_coordinates(location):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if len(data) == 0:
        raise ValueError("Location was not found.")

    return data[0]["lat"], data[0]["lon"]


def get_weather(location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise ValueError("Weather data was not found.")

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    return temp, description, humidity


def get_uv(lat, lon):
    url = f"https://api.openuv.io/api/v1/uv?lat={lat}&lng={lon}"
    headers = {"x-access-token": OPENUV_API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    if "result" not in data:
        raise ValueError("UV data was not found.")

    return data["result"]["uv"]


def get_aqi(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={AQICN_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        raise ValueError("AQI data was not found.")

    aqi = data["data"]["aqi"]

    if aqi == "-":
        return 0

    return int(aqi)


def get_forecast_list(location):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise ValueError("Forecast data was not found.")

    timezone_offset = data["city"]["timezone"]
    forecasts = []

    for item in data["list"][:16]:
        local_time = datetime.fromtimestamp(item["dt"] + timezone_offset, timezone.utc)

        forecast = {
            "time": local_time.strftime("%Y-%m-%d %I:%M %p").replace(" 0", " "),
            "hour": int(local_time.strftime("%H")),
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"]
        }

        forecasts.append(forecast)

    return forecasts