import json
import datetime as dt

from sentinel import get_latest_scene
from sentinel_process import download_preview

from oil_detector import (
    detect_dark_spots,
    risk_score
)

from shape_analysis import analyze_shape

from oil_probability import oil_probability

from geo_utils import pixel_to_geo

from ais_reader import load_vessels

from vessel_correlation import (
    find_nearest_vessel,
    vessel_risk_score
)

from oil_spill_map import create_oil_spill_map



def load_config():

    with open(
        "config.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



print(
    "=================================================="
)

print(
    "Oil Spill Intelligence V2"
)

print(
    "=================================================="
)



cfg = load_config()



print("\n📡 Loading AIS Cache...")

vessels = load_vessels()

print(
    "AIS Vessels Loaded:",
    len(vessels)
)



for area in cfg["areas"]:


    print(
        f"\n📍 المنطقة: {area['name_ar']}"
    )


    scene = get_latest_scene(

        area["bbox"],

        cfg["lookback_hours"]

    )


    if scene is None:

        print(
            "No Sentinel-1 scene found."
        )

        continue



    print(
        "Scene:"
    )

    print(
        scene["id"]
    )



    scene_time = dt.datetime.fromisoformat(

        scene["properties"]["datetime"]
        .replace(
            "Z",
            "+00:00"
        )

    )



    img = download_preview(

        area["bbox"],

        scene_time - dt.timedelta(
            minutes=10
        ),

        scene_time + dt.timedelta(
            minutes=10
        )

    )



    if img is None:

        print(
            "Image download failed."
        )

        continue



    print(
        "Image:",
        img.shape
    )



    result = detect_dark_spots(
        img
    )



    if result is None:

        print(
            "\n🟢 No dark spot detected."
        )

        continue



    score = risk_score(
        result["ratio"]
    )



    print(
        "\n🚨 Detection Result"
    )

    print(
        "----------------------"
    )

    print(
        f"Area             : {result['area']/10000:.3f} km²"
    )

    print(
        f"Risk Score       : {score}/100"
    )



    confidence = min(
        result["ratio"] * 100 * 10,
        99
    )


    print(
        f"Confidence       : {confidence:.2f}%"
    )



    lat, lon = pixel_to_geo(

        result["center"][1],

        result["center"][0],

        area["bbox"],

        img.shape

    )



    print(
        "\n📍 Location"
    )

    print(
        "----------------------"
    )

    print(
        f"Latitude         : {lat}"
    )

    print(
        f"Longitude        : {lon}"
    )



    shape = analyze_shape(
        result["mask"]
    )



    print(
        "\n🔬 Shape Analysis"
    )

    print(
        "----------------------"
    )


    for k, v in shape.items():

        print(
            f"{k.capitalize():16}: {v}"
        )



    probability = oil_probability(

        result["ratio"],

        shape

    )



    print(
        "\n🛢 Oil Spill Probability"
    )

    print(
        "----------------------"
    )

    print(
        f"Probability      : {probability}%"
    )



    nearest = find_nearest_vessel(

        lat,

        lon,

        vessels

    )



    print(
        "\n🚢 Vessel Correlation"
    )

    print(
        "----------------------"
    )


    vessel_score = 0


    if nearest:


        print(
            f"Nearest Vessel : {nearest.get('name')}"
        )

        print(
            f"Distance       : {nearest.get('distance_km')} km"
        )

        print(
            f"Speed          : {nearest.get('speed')} knots"
        )


        vessel_score = vessel_risk_score(
            nearest
        )


        print(
            f"Vessel Risk    : +{vessel_score}"
        )


    else:

        print(
            "Nearest Vessel : None"
        )



    final_probability = min(

        probability + vessel_score,

        99

    )


    print(
        "\n🛢 Final Oil Spill Assessment"
    )

    print(
        "----------------------"
    )

    print(
        f"Satellite Probability : {probability}%"
    )

    print(
        f"Vessel Contribution  : +{vessel_score}%"
    )

    print(
        f"Final Probability    : {final_probability}%"
    )



    print(
        "\n🗺️ Creating Map..."
    )


    create_oil_spill_map(

        lat,

        lon,

        final_probability

    )


    print(
        "🗺️ Map Created"
    )



print(
    "\n=================================================="
)

print(
    "Finished"
)

print(
    "=================================================="
)
