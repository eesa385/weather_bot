import requests
import datetime
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CITY = "Faisalabad"
API_URL = f"https://wttr.in/{CITY}?format=j1"

def fetch_weather():
    response = requests.get(API_URL)
    data = response.json()

    current = data["current_condition"][0]
    return {
        "temp": current["temp_C"],
        "condition": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind": current["windspeedKmph"]
    }

def send_to_discord(weather):
    now = datetime.datetime.now().strftime('%I:%M %p - %d %b %Y')
    message = (
        f"🌤️ **Weather in Faisalabad**\n"
        f"🕖 Time: {now}\n\n"
        f"🌡️ Temp: {weather['temp']}°C\n"
        f"☁️ Condition: {weather['condition']}\n"
        f"💧 Humidity: {weather['humidity']}%\n"
        f"💨 Wind: {weather['wind']} km/h"
    )
    payload = {"content": message}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        raise Exception(f"Discord error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    weather = fetch_weather()
    send_to_discord(weather)
