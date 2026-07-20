import json
import datetime as dt

from sentinel import get_latest_scene
from sentinel_process import download_preview
from oil_detector import detect_dark_spots, risk_score, confidence



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




    if not result["detected"]:

        print("🟢 No dark spot detected.")

        continue




    risk = risk_score(

        result["ratio"]

    )


    conf = confidence(

        result["ratio"]

    )



    print("\n🔎 Analysis")

    print("----------------------")

    print(
        f"Dark Area Pixels: {result['area_pixels']:,}"
    )


    print(
        f"Dark Ratio      : {result['ratio']:.4%}"
    )


    print(
        f"Risk Level      : {risk['level']}"
    )


    print(
        f"Risk Score      : {risk['score']}/100"
    )


    print(
        f"Confidence      : {conf}%"
    )


    print(
        f"Center          : {result['center']}"
    )



print("\n==================================================")

print("Finished")

print("==================================================")
