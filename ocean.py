import requests

# البحر الأحمر (يمكن تغييرها لاحقاً)
LAT = 22.5
LON = 38.8


def current_direction(deg):
    dirs = [
        "شمالي", "شمال شرقي", "شرقي", "جنوب شرقي",
        "جنوبي", "جنوب غربي", "غربي", "شمال غربي"
    ]
    return dirs[round(deg / 45) % 8]


def get_ocean():

    url = (
        "https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        "&hourly=ocean_current_velocity,ocean_current_direction"
        "&forecast_days=1"
    )

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    data = r.json()

    speed = data["hourly"]["ocean_current_velocity"][0]
    direction = data["hourly"]["ocean_current_direction"][0]

    return {
        "speed": speed,
        "direction_deg": direction,
        "direction_ar": current_direction(direction)
    }


if __name__ == "__main__":

    info = get_ocean()

    print("=" * 40)
    print("Ocean Current Intelligence")
    print("=" * 40)
    print(f"Speed      : {info['speed']} m/s")
    print(f"Direction  : {info['direction_deg']}°")
    print(f"Arabic     : {info['direction_ar']}")
