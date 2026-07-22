import os
import asyncio
import ssl
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


async def test_ais():

    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )

    print(
        "AIS KEY EXISTS:",
        bool(api_key),
        "LENGTH:",
        len(api_key) if api_key else 0
    )


    if not api_key:
        print("❌ Missing API Key")
        return


    ssl_context = ssl.create_default_context()


    try:

        print("📡 Connecting AISStream...")


        async with websockets.connect(

            AISSTREAM_URL,

            ssl=ssl_context,

            open_timeout=60,

            ping_interval=20,

            ping_timeout=60,

            close_timeout=30

        ) as ws:


            print(
                "✅ Connected"
            )


            message = {

                "APIKey": api_key,

                "BoundingBoxes": [

                    [
                        [
                            49.0,
                            24.0
                        ],
                        [
                            50.0,
                            25.0
                        ]
                    ]

                ],

                "FilterMessageTypes": [

                    "PositionReport"

                ]

            }


            import json

            await ws.send(
                json.dumps(message)
            )


            print(
                "✅ Subscription Sent"
            )


            try:

                data = await asyncio.wait_for(

                    ws.recv(),

                    timeout=30

                )


                print(
                    "📩 Message Received"
                )

                print(
                    data[:200]
                )


            except asyncio.TimeoutError:

                print(
                    "⚠️ Connected but no vessel message in 30 seconds"
                )


    except Exception as e:

        print(
            "❌ AIS Error:",
            e
        )


if __name__ == "__main__":

    asyncio.run(
        test_ais()
    )
