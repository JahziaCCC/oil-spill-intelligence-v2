from sentinel import get_latest_scene

scene = get_latest_scene()

print("=" * 50)

if scene:
    print("Latest Sentinel-1 Scene")
    print(scene["scene"])
    print(scene["time"])
else:
    print("No Scene Found")

print("=" * 50)
