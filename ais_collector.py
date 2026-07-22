import os
import json
import asyncio
import ssl
import websockets

from datetime import datetime, timezone


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream/"

CACHE_FILE = "ais_cache.json"


# الخليج العربي + البحر الأحمر
BBOX = [
    [
        [
            34.0,
            15.0
        ],
        [
            55.0,
            30.0
        ]
    ]
]


COLLECT_SECONDS = 120



def save_cache(vessels):

    data = {

        "updated":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "count":
            len(vessels),

        "vessels":
            vessels

    }


    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



async def connect_ais():


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print(
            "❌ AISSTREAM_API_KEY missing"
        )

        return []



    subscribe_message = {

        "APIKey":
            api_key,

        "BoundingBoxes":
            BBOX,

        "FilterMessageTypes":
            [
                "PositionReport"
            ]

    }



    ssl_context = ssl.create_default_context()

    ssl_context.check_hostname = False

    ssl_context.verify_mode = ssl.CERT_NONE



    vessels = []



    for attempt in range(1, 4):

        try:

            print(
                f"📡 AIS Connection Attempt {attempt}/3"
            )


            async with websockets.connect(

                AISSTREAM_URL,

                ssl=ssl_context,

                open_timeout=60,

                close_timeout=20,

                ping_interval=30,

                ping_timeout=120,

                max_size=None

            ) as websocket:


                print(
                    "✅ AIS Connected"
                )


                await websocket.send(

                    json.dumps(
                        subscribe_message
                    )

                )


                start = asyncio.get_event_loop().time()



                while (

                    asyncio.get_event_loop().time()
                    -
                    start

                    <

                    COLLECT_SECONDS

                ):


                    try:


                        message = await asyncio.wait_for(

                            websocket.recv(),

                            timeout=10

                        )


                        data = json.loads(
                            message
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
                                    ),


                                "heading":
                                    position.get(
                                        "Cog",
                                        0
                                    )

                            }



                            vessels.append(
                                vessel
                            )


                            print(
                                "🚢",
                                vessel
                            )



                    except asyncio.TimeoutError:

                        continue



                return vessels



        except Exception as e:


            print(
                f"❌ AIS Attempt {attempt} Failed:",
                e
            )


            await asyncio.sleep(
                10
            )



    print(
        "⚠️ AIS unavailable - continue without vessels"
    )


    return []




async def collect_ais():


    print(
        "📡 AIS Collector Starting..."
    )


    vessels = await connect_ais()



    print(
        "AIS Vessels Received:",
        len(vessels)
    )



    if vessels:


        save_cache(
            vessels
        )


        print(
            "✅ ais_cache.json updated"
        )


    else:


        print(
            "⚠️ No vessels received"
        )



if __name__ == "__main__":


    asyncio.run(
        collect_ais()
    )
