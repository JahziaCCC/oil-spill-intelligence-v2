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



    if "valid_objects" in stats:

        print(f"Valid Objects   : {stats['valid_objects']}")



    if not result["detected"]:

        print("\n🟢 No dark spot detected.")

        continue



    risk = risk_score(
        result["ratio"]
    )


    conf = confidence(
        result["ratio"]
    )



    area_km2 = estimate_area_km2(
        result["area_pixels"],
        area["bbox"],
        img.shape
    )



    shape = analyze_shape(
        result["mask"]
    )



    probability = calculate_oil_probability(

        dark_ratio=result["ratio"],

        area_km2=area_km2,

        elongation=shape["elongation"],

        compactness=shape["compactness"],

        confidence=conf

    )



    location = pixel_to_geo(

        result["center"][0],

        result["center"][1],

        area["bbox"],

        img.shape

    )



    print("\n🚨 Detection Result")
    print("----------------------")

    print(f"Dark Area Pixels : {result['area_pixels']:,}")

    print(f"Estimated Area   : {area_km2:.3f} km²")

    print(f"Dark Ratio       : {result['ratio']:.4%}")

    print(f"Risk Level       : {risk['level']}")

    print(f"Risk Score       : {risk['score']}/100")

    print(f"Confidence       : {conf}%")

    print(f"Center Pixel     : {result['center']}")



    print("\n📍 Location")

    print("----------------------")

    print(
        f"Latitude         : {location['latitude']}"
    )

    print(
        f"Longitude        : {location['longitude']}"
    )



    print("\n🔬 Shape Analysis")

    print("----------------------")

    print(f"Perimeter        : {shape['perimeter']}")

    print(f"Elongation       : {shape['elongation']}")

    print(f"Compactness      : {shape['compactness']}")



    print("\n🛢 Oil Spill Probability")

    print("----------------------")

    print(
        f"Probability      : {probability['probability']}%"
    )

    print(
        f"Classification   : {probability['classification']}"
    )




print("\n==================================================")
print("Finished")
print("==================================================")
