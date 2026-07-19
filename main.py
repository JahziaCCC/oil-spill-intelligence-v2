from weather import get_weather
from ocean import get_ocean

# رأس تنورة (اختبار)
LAT = 26.6436
LON = 50.1591

weather = get_weather(LAT, LON)
ocean = get_ocean()

print("=" * 50)
print("Oil Spill Intelligence V2")
print("=" * 50)

print("💨 Weather")
print(f"Speed      : {weather['speed']} m/s")
print(f"Direction  : {weather['direction_deg']}°")
print(f"Arabic     : {weather['direction_text']}")

print()

print("🌊 Ocean Current")
print(f"Speed      : {ocean['speed']} m/s")
print(f"Direction  : {ocean['direction_deg']}°")
print(f"Arabic     : {ocean['direction_ar']}")

print("=" * 50)
