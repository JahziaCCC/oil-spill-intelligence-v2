import os
import requests
import datetime as dt

TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
CATALOG_URL = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0/search"


def get_token():
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["CDSE_CLIENT_ID"],
            "client_secret": os.environ["CDSE_CLIENT_SECRET"],
        },
        timeout=30,
    )

    r.raise_for_status()
    return r.json()["access_token"]


def get_latest_scene():

    token = get_token()

    now = dt.datetime.utcnow()
    start = now - dt.timedelta(days=3)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "collections": ["sentinel-1-grd"],
        "datetime": f"{start.isoformat()}Z/{now.isoformat()}Z",
        "bbox": [47.5, 24.0, 56.5, 30.8],   # الخليج العربي
        "limit": 1
    }

    r = requests.post(
        CATALOG_URL,
        headers=headers,
        json=body,
        timeout=60
    )

    r.raise_for_status()

    features = r.json()["features"]

    if len(features) == 0:
        return None

    return {
        "scene": features[0]["id"],
        "time": features[0]["properties"]["datetime"]
    }


if __name__ == "__main__":

    scene = get_latest_scene()

    if scene:
        print("Latest Scene")
        print(scene["scene"])
        print(scene["time"])
    else:
        print("No scene found")
