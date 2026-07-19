import os
import datetime as dt
import requests

TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
BASE_URL = "https://sh.dataspace.copernicus.eu"

CATALOG_SEARCH = f"{BASE_URL}/api/v1/catalog/1.0.0/search"
PROCESS_API = f"{BASE_URL}/api/v1/process"


def utc_now():
    return dt.datetime.now(dt.timezone.utc)


def iso_z(d):
    return d.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def get_token():

    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["CDSE_CLIENT_ID"],
            "client_secret": os.environ["CDSE_CLIENT_SECRET"],
        },
        timeout=60,
    )

    r.raise_for_status()

    return r.json()["access_token"]


def get_latest_scene(bbox, hours=72):

    token = get_token()

    end = utc_now()
    start = end - dt.timedelta(hours=hours)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "collections": ["sentinel-1-grd"],
        "bbox": bbox,
        "datetime": f"{iso_z(start)}/{iso_z(end)}",
        "limit": 1,
        "fields": {
            "include": [
                "id",
                "properties.datetime"
            ]
        }
    }

    r = requests.post(
        CATALOG_SEARCH,
        headers=headers,
        json=body,
        timeout=120
    )

    r.raise_for_status()

    features = r.json().get("features", [])

    if not features:
        return None

    return features[0]
