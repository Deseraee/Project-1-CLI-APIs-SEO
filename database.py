import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

connection = sqlite3.connect("mydatabase.db")
curr = connection.cursor()

username = input("Enter your username: ")
name = input("Enter your name: ")
location = input("Enter your location: ")

curr.execute(
  "INSERT INTO usersInfo (username, name, location) VALUES (?, ?, ?)",
  (username,name,location)
)

url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
respond = requests.get(url)
location_weather = respond.json()

if respond.status_code == 200:
  temperature = location_weather["main"]["temp"]
  description = location_weather["weather"][0]["description"]
  humidity = location_weather["main"]["humidity"] 
  
  print(f"The weather in your location is {temperature}°C, with {description}, and a humidity of {humidity}%")



connection.commit()
connection.close()

