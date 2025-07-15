import requests
import datetime
import os

# Constants
CITY = "Faisalabad"
API_KEY = os.getenv("WEATHER_API_KEY")  # Stored in GitHub Secrets
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Stored in GitHub Secrets

def fetch_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=yes"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Weather API error: {response.text}")
    
    data = response.json()
    current = data['current']
    condition = current['condition']['text']
    temp = current['temp_c']
    humidity = current['humidity']
    wind = current['wind_kph']
    aqi = current.get('air_quality', {}).get('pm2_5', 'N/A')  # PM2.5 AQI reading

    return {
        "condition": condition,
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "aqi": round(aqi, 1) if aqi != 'N/A' else 'N/A'
    }

def send_to_discord(weather):
    now = datetime.datetime.now().strftime('%I:%M %p - %d %b %Y')
    message = (
        f"🌦️ **Daily Weather Update - Faisalabad**\n"
        f"🕖 **Time**: {now}\n\n"
        f"🌡️ Temperature: {weather['temp']}°C\n"
        f"🌤️ Condition: {weather['condition']}\n"
        f"💧 Humidity: {weather['humidity']}%\n"
        f"💨 Wind Speed: {weather['wind']} km/h\n"
        f"🫧 Air Quality (PM2.5): {weather['aqi']}\n"
    )
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        raise Exception(f"Discord webhook error: {response.text}")

if __name__ == "__main__":
    weather = fetch_weather()
    send_to_discord(weather)
