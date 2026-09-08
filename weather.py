import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_current_weather(latitude: float, longitude: float) -> dict:
    """
    Get the current weather for a geographic location.

    Args:
        latitude: Geographic latitude.
        longitude: Geographic longitude.

    Returns:
        Current temperature, feels like temperature, humidity,
        weather description and wind speed.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }
def get_forecast(latitude: float, longitude: float) -> list:
    """
    Get the weather forecast for tomorrow.

    Args:
        latitude: Geographic latitude.
        longitude: Geographic longitude.

    Returns:
        Weather forecast data for tomorrow.
    """

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    tomorrow = datetime.now().date() + timedelta(days=1)

    forecasts = []

    for item in data["list"]:

        date = datetime.fromtimestamp(item["dt"]).date()

        if date == tomorrow:

            forecasts.append({
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"]
            })

    return forecasts

def summarize_tomorrow(forecasts):

    if not forecasts:
        return None

    temperatures = [
        item["temperature"]
        for item in forecasts
    ]

    descriptions = [
        item["description"]
        for item in forecasts
    ]

    return {
        "min": min(temperatures),
        "max": max(temperatures),
        "description": descriptions[len(descriptions) // 2]
    }
