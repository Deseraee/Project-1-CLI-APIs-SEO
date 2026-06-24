import sqlite3
import requests
import os
import dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

connection = sqlite3.connect("mydatabase.db")
curr = connection.cursor()

username = input("Enter your username: ")
name = input("Enter your name: ")
location = input("Enter your location: ")

curr.execute(
  "INSERT INTO usersInfo (username, name, location) VALUES (?, ?, ?)",
  (username,name,location)
)


#if the username is already in the databse it ask the user if their location
# is the current one assoicated with the username 
# yes - same user
#no new user and tell me that username is already taken
#if username in databse:
 # reply = input("Is your location {location} ? yes or no: ")
  #curr.execute("INSERT INTO usersInfo")

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

