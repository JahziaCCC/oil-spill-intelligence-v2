import time
import json

print("⏳ Waiting for AIS messages...")

received = 0
start_time = time.time()

while time.time() - start_time < 30:

    try:
        message = ws.recv()

        data = json.loads(message)

        print("=" * 60)
        print("📥 AIS MESSAGE")
        print(json.dumps(data, indent=2))

        received += 1

        if received >= 5:
            break

    except Exception as e:
        print("Receive Error:", e)
        break

if received == 0:
    print("⚠️ No AIS messages received within 30 seconds.")
 بناء على الشات السابق 
