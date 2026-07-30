import os
import json
import time
import websocket

AIS_API_KEY = os.getenv("AISSTREAM_API_KEY")

print("AIS KEY EXISTS:", AIS_API_KEY is not None,
      "LENGTH:", len(AIS_API_KEY) if AIS_API_KEY else 0)

if not AIS_API_KEY:
    raise Exception("AIS_API_KEY not found")


print("📡 Connecting AISStream...")

ws = websocket.create_connection(
    "wss://stream.aisstream.io/v0/stream",
    timeout=15
)

print("✅ AIS Connected")

subscribe_message = {
    "APIKey": AIS_API_KEY,
    "BoundingBoxes": [

        # مضيق هرمز
        [
            [25.5, 55.0],
            [27.5, 57.0]
        ],

        # باب المندب
        [
            [12.0, 42.5],
            [13.5, 44.5]
        ],

        # قناة السويس
        [
            [29.5, 31.5],
            [31.0, 33.0]
        ]

    ]
}

ws.send(json.dumps(subscribe_message))

print("✅ Test message sent")
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

else:

    print(f"✅ Total AIS messages received: {received}")

ws.close()

print("🔌 Connection closed")
