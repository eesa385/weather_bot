import requests
import datetime
import os

# Constants
CITY = "Faisalabad"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    data = response.json()
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description'].title()

    return {
        'temp': temp,
        'humidity': humidity,
        'wind': wind_speed,
        'description': description
    }

def send_to_discord(weather):
    now = datetime.datetime.now().strftime('%I:%M %p - %d %b %Y')
    message = (
        f"🌦️ **Weather Update - Faisalabad**\n"
        f"🕖 **Time**: {now}\n\n"
        f"🌡️ Temperature: {weather['temp']}°C\n"
        f"🌤️ Condition: {weather['description']}\n"
        f"💧 Humidity: {weather['humidity']}%\n"
        f"💨 Wind Speed: {weather['wind']} m/s"
    )
    payload = {"content": message}
    
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        raise Exception(f"Discord webhook error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    weather = fetch_weather()
    send_to_discord(weather)
