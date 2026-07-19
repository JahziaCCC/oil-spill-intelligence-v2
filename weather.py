import requests

def degrees_to_direction(deg):
    directions = [
        "شمال",
        "شمال شرقي",
        "شرق",
        "جنوب شرقي",
        "جنوب",
        "جنوب غربي",
        "غرب",
        "شمال غربي"
    ]

    index = int((deg + 22.5) // 45) % 8
    return directions[index]


def get_weather(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=wind_speed_10m,wind_direction_10m"
    )

    r = requests.get(url, timeout=20)
    r.raise_for_status()

    current = r.json()["current"]

    direction_deg = current["wind_direction_10m"]

    return {
        "speed": current["wind_speed_10m"],
        "direction_deg": direction_deg,
        "direction_text": degrees_to_direction(direction_deg)
    }
