from sentinel import get_latest_scene
from sentinel_process import download_preview
from oil_detector import detect_dark_spots, risk_score

import datetime as dt

print("==================================================")
print("Oil Spill Intelligence V2")
print("==================================================")

# الخليج العربي
bbox = [47.0, 23.0, 56.8, 30.8]

scene = get_latest_scene(bbox)

if scene is None:
    print("No Sentinel-1 scene found.")
    exit()

print("Scene:")
print(scene["id"])

scene_time = dt.datetime.fromisoformat(
    scene["properties"]["datetime"].replace("Z", "+00:00")
)

img = download_preview(
    bbox,
    scene_time - dt.timedelta(minutes=10),
    scene_time + dt.timedelta(minutes=10),
)

print("")
print("Image downloaded successfully.")
print("Image shape:", img.shape)

# ====================================
# تحليل الصورة
# ====================================

result = detect_dark_spots(img)

print("")
print("========== Analysis ==========")

if result is None:

    print("No dark spot detected")

else:

    score = risk_score(result["ratio"])

    print(f"Dark Area : {result['area']:,} pixels")
    print(f"Dark Ratio: {result['ratio']:.4%}")
    print(f"Risk Score: {score}/100")
    print(f"Center    : {result['center']}")

print("==============================")
