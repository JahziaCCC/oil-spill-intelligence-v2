import os
import json
import time
import websocket


AIS_API_KEY = os.getenv("AISSTREAM_API_KEY")


print(
    "AIS KEY EXISTS:",
    AIS_API_KEY is not None,
    "LENGTH:",
    len(AIS_API_KEY) if AIS_API_KEY else 0
)


if not AIS_API_KEY:
    raise Exception("AISSTREAM_API_KEY not found")


print("📡 Connecting AISStream...")


ws = websocket.create_connection(
    "wss://stream.aisstream.io/v0/stream",
    timeout=30
)


print("✅ AIS Connected")


subscribe_message = {

    "APIKey": AIS_API_KEY,

    "BoundingBoxes": [

        [
            [
                10.0,
                30.0
            ],
            [
                35.0,
                60.0
            ]
        ]

    ],

    "FilterMessageTypes": [

        "PositionReport"

    ]

}


ws.send(
    json.dumps(subscribe_message)
)


print(
    "✅ Subscription sent"
)

print(
    "⏳ Waiting for AIS messages (120 seconds)..."
)


received = 0

start_time = time.time()


while time.time() - start_time < 120:

    try:

        message = ws.recv()


        data = json.loads(
            message
        )


        print("=" * 60)

        print(
            "📥 AIS MESSAGE RECEIVED"
        )


        metadata = data.get(
            "MetaData",
            {}
        )


        position = data.get(
            "Message",
            {}
        )


        print(
            json.dumps(
                metadata,
                indent=2
            )
        )


        print(
            json.dumps(
                position,
                indent=2
            )
        )


        received += 1


        if received >= 5:

            break



    except Exception as e:


        print(
            "Receive Error:",
            e
        )

        break



if received == 0:

    print(
        "⚠️ No AIS messages received within 120 seconds."
    )


else:

    print(
        f"✅ Total AIS messages received: {received}"
    )



ws.close()


print(
    "🔌 Connection closed"
)
