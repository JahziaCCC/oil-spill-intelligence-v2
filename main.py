from sentinel import get_latest_scene

print("==================================================")
print("Latest Sentinel-1 Scene")
print("==================================================")

# الخليج العربي
bbox = [47.0, 23.0, 56.8, 30.8]

scene = get_latest_scene(bbox)

if scene:
    print(scene["id"])
    print(scene["properties"]["datetime"])
else:
    print("No scene found")

print("==================================================")
