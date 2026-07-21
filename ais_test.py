import os
import json
import asyncio
import ssl
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


async def test_ais():

    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print(
            "❌ AISSTREAM_API_KEY missing"
        )

        return



    ssl_context = ssl.create_default_context()

    ssl_context.check_hostname = False

    ssl_context.verify_mode = ssl.CERT_NONE



    # نطاق واسع للاختبار
    # الخليج العربي + البحر الأحمر

    subscribe_message = {

        "APIKey": api_key,

        "BoundingBoxes": [

            [
                [
                    30.0,
                    10.0
                ],

                [
                    60.0,
                    35.0
                ]
            ]

        ],

        "FilterMessageTypes": [

            "PositionReport"

        ]

    }



    vessels = []



    try:


        print(
            "📡 Connecting AISStream..."
        )


        async with websockets.connect(

            AISSTREAM_URL,

            ssl=ssl_context,

            open_timeout=30,

            ping_interval=20,

            ping_timeout=60

        ) as websocket:


            print(
                "✅ Connected"
            )



            await websocket.send(

                json.dumps(
                    subscribe_message
                )

            )


            print(
                "⏳ Waiting for vessels..."
            )



            start = asyncio.get_event_loop().time()



            while (

                asyncio.get_event_loop().time()
                -
                start

                <

                60

            ):


                try:


                    msg = await asyncio.wait_for(

                        websocket.recv(),

                        timeout=10

                    )


                    data = json.loads(
                        msg
                    )



                    metadata = data.get(
                        "MetaData",
                        {}
                    )


                    position = data.get(
                        "Message",
                        {}
                    ).get(
                        "PositionReport"
                    )


                    if position:


                        vessel = {

                            "name":
                                metadata.get(
                                    "ShipName",
                                    "Unknown"
                                ),

                            "mmsi":
                                metadata.get(
                                    "MMSI"
                                ),

                            "lat":
                                position.get(
                                    "Latitude"
                                ),

                            "lon":
                                position.get(
                                    "Longitude"
                                ),

                            "speed":
                                position.get(
                                    "Sog",
                                    0
                                )
                        }


                        vessels.append(
                            vessel
                        )


                        print(
                            "🚢 Vessel:",
                            vessel
                        )



                except asyncio.TimeoutError:

                    continue



        print()
        print(
            "=============================="
        )

        print(
            "Total Vessels:",
            len(vessels)
        )

        print(
            "=============================="
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
