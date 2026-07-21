import json
import datetime as dt

from sentinel import get_latest_scene
from sentinel_process import download_preview

from oil_detector import (
    detect_dark_spots,
    risk_score,
    confidence
)

from geo_utils import estimate_area_km2

from shape_analysis import analyze_shape

from oil_probability import calculate_oil_probability

from geo_location import pixel_to_geo

from oil_spill_map import create_oil_spill_map

from ais_correlation import (
    find_nearest_vessel,
    vessel_risk_score
)



def load_config():

    with open("config.json", "r", encoding="utf-8") as f:

        return json.load(f)



print("==================================================")
print("Oil Spill Intelligence V2")
print("==================================================")


cfg = load_config()



for area in cfg["areas"]:


    print(f"\n📍 المنطقة: {area['name_ar']}")



    scene = get_latest_scene(
        area["bbox"],
        cfg["lookback_hours"]
    )


    if scene is None:

        print("No Sentinel-1 scene found.")

        continue



    print("Scene:")
    print(scene["id"])



    scene_time = dt.datetime.fromisoformat(
        scene["properties"]["datetime"].replace(
            "Z",
            "+00:00"
        )
    )



    img = download_preview(
        area["bbox"],
        scene_time - dt.timedelta(minutes=10),
        scene_time + dt.timedelta(minutes=10)
    )



    if img is None:

        print("Image download failed.")

        continue



    print("Image:", img.shape)



    result = detect_dark_spots(img)

    stats = result["stats"]



    print("\n🔎 Analysis Summary")
    print("----------------------")

    print(f"Image Mean      : {stats['image_mean']}")
    print(f"Min Value       : {stats['image_min']}")
    print(f"Max Value       : {stats['image_max']}")
    print(f"Dark Threshold  : {stats['threshold']}")
    print(f"Candidate Pixels: {stats['candidate_pixels']:,}")
    print(f"Objects Found   : {stats['objects_found']}")



    if not result["detected"]:

        print("\n🟢 No dark spot detected.")

        continue



    risk = risk_score(result["ratio"])

    conf = confidence(result["ratio"])



    area_km2 = estimate_area_km2(
        result["area_pixels"],
        area["bbox"],
        img.shape
    )



    shape = analyze_shape(result["mask"])



    location = pixel_to_geo(
        result["center"][0],
        result["center"][1],
        area["bbox"],
        img.shape
    )



    probability = calculate_oil_probability(

        dark_ratio=result["ratio"],

        area_km2=area_km2,

        elongation=shape["elongation"],

        compactness=shape["compactness"],

        confidence=conf

    )



    print("\n🚨 Detection Result")
    print("----------------------")

    print(f"Area             : {area_km2:.3f} km²")
    print(f"Risk Score       : {risk['score']}/100")
    print(f"Confidence       : {conf}%")



    print("\n📍 Location")
    print("----------------------")

    print(
        f"Latitude         : {location['latitude']}"
    )

    print(
        f"Longitude        : {location['longitude']}"
    )



    print("\n🚢 Vessel Correlation")
    print("----------------------")



    # بيانات اختبار مؤقتة
    vessels = [

        {
            "name": "Test Vessel A",
            "imo": "123456789",
            "lat": 24.35,
            "lon": 49.91,
            "speed": 8
        }

    ]



    nearest = find_nearest_vessel(

        location["latitude"],

        location["longitude"],

        vessels

    )



    vessel_score = vessel_risk_score(
        nearest
    )



    if nearest:

        print(
            f"Nearest Vessel : {nearest['name']}"
        )

        print(
            f"Distance       : {nearest['distance_km']} km"
        )

        print(
            f"Speed          : {nearest['speed']} knots"
        )

        print(
            f"Vessel Risk    : +{vessel_score}"
        )

    else:

        print(
            "Nearest Vessel : None"
        )



    final_probability = min(

        100,

        probability["probability"] + vessel_score

    )



    print("\n🛢 Final Oil Spill Assessment")

    print("----------------------")

    print(
        f"Satellite Probability : {probability['probability']}%"
    )

    print(
        f"Vessel Contribution  : +{vessel_score}%"
    )

    print(
        f"Final Probability    : {final_probability}%"
    )



    create_oil_spill_map(

        latitude=location["latitude"],

        longitude=location["longitude"],

        area_km2=area_km2,

        probability=final_probability,

        classification=probability["classification"],

        confidence=conf,

        scene_id=scene["id"]

    )



    print("\n🗺️ Map Created")




print("\n==================================================")
print("Finished")
print("==================================================")
