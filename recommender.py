# recommender.py - decides if an outdoor activity is safe
import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
OPENUV_API_KEY = os.getenv("OPENUV_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

connection = sqlite3.connect("mydatabase.db")
curr = connection.cursor()
curr.execute("SELECT location FROM usersInfo ORDER BY id DESC LIMIT 1")
location = curr.fetchone()[0]
connection.close()

coordinates_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_API_KEY}"
c = requests.get(coordinates_url).json()
lat = c[0]["lat"]
lon = c[0]["lon"]


url = f'https://api.openuv.io/api/v1/uv?lat={lat}&lng={lon}'
headers = {'x-access-token': OPENUV_API_KEY}
respond = requests.get(url, headers=headers)
data_uv = respond.json()
uv = data_uv['result']['uv']


temp_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
respond = requests.get(temp_url)
temp_d = respond.json()
temp = temp_d['main']['temp']

aqi = 50 

def get_recommendation(activity, temp, aqi, uv):
    activity = activity.lower()
    score = 0
    reasons = []

    # Air quality
    if aqi >= 150:
        score += 3
        reasons.append("Air quality is unhealthy")
    elif aqi >= 100:
        score += 2
        reasons.append("Air quality may be unhealthy for sensitive people")
    elif aqi >= 50:
        score += 1
        reasons.append("Air quality is moderate")

    # UV index
    if uv >= 8:
        score += 2
        reasons.append("UV index is very high")
    elif uv >= 6:
        score += 1
        reasons.append("UV index is high")

    # Temperature
    if temp >= 95:
        score += 2
        reasons.append("Temperature is very hot")
    elif temp >= 85:
        score += 1
        reasons.append("Temperature is hot")

    # Activity-specific risks
    if activity == "golf" and uv >= 6:
        score += 1
        reasons.append("Golf usually means long sun exposure")

    if activity == "run" and aqi >= 100:
        score += 1
        reasons.append("Running is harder on the lungs when air quality is poor")

    if not reasons:
        reasons.append("Conditions look generally safe")

    # Final verdict
    if score <= 2:
        verdict = "GOOD"
    elif score <= 5:
        verdict = "CAUTION"
    else:
        verdict = "AVOID"

    return verdict, reasons

activity = input(f"What activity are you doing today?: ")
verdict, reasons = get_recommendation(activity, temp, aqi, uv)

print(f"Verdict: {verdict}")