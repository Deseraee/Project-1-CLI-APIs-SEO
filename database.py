import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
def user_report(username, location, activity, temp, description, humidity, aqi, uv, verdict, reasons, forecast_time, forecast_temp, forecast_description, time, vehicle):
  connection = sqlite3.connect("mydatabase.db")
  curr = connection.cursor()
  curr.execute(
    "INSERT INTO WeatherReport (username, location, activity, current_temperature, current_weather, humidity, aqi, uv_index, verdict, reasons, forecast_time, forecast_temperature, forecast_weather, time, vehicle) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (
      username,
      location,
      activity,
      temp,
      description,
      humidity,
      aqi,
      uv,
      verdict,
      "; ".join(reasons),
      forecast_time,
      forecast_temp,
      forecast_description,
      time,
      vehicle
    ))

  connection.commit()
  connection.close()

