#V2 start
import requests


def get_location():
    response = requests.get("https://ipinfo.io/json", timeout=5)
    response.raise_for_status()

    data = response.json()

    return {
        "city": data["city"],
        "country": data["country"],
        "latitude": float(data["loc"].split(",")[0]),
        "longitude": float(data["loc"].split(",")[1])
    }
#V2 end