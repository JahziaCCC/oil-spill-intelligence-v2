from weather import get_weather

# رأس تنورة (تجربة)
LAT = 26.6436
LON = 50.1591

weather = get_weather(LAT, LON)

print("=" * 40)
print("Oil Spill Intelligence V2")
print("=" * 40)

print(f"Wind Speed : {weather['speed']} m/s")
print(f"Direction  : {weather['direction_deg']}°")
print(f"Arabic     : {weather['direction_text']}")
