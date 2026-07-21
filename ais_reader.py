import json
import os


CACHE_FILE = "ais_cache.json"


def load_vessels():

    if not os.path.exists(CACHE_FILE):
        print("⚠️ AIS cache not found")
        return []


    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        vessels = data.get(
            "vessels",
            []
        )


        print(
            "🚢 Cached Vessels:",
            len(vessels)
        )


        return vessels


    except Exception as e:

        print(
            "❌ AIS cache error:",
            e
        )

        return []
