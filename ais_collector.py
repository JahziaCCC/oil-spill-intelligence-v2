import os
import json
import asyncio
import ssl
import websockets
from datetime import datetime, timezone


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

CACHE_FILE = "ais_cache.json"


# نطاق واسع:
# الخليج العربي + البحر الأحمر

BBOX = [
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



async def collect_ais():


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print(
            "❌ AISSTREAM_API_KEY missing"
        )

        return



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



    try:


        print(
            "📡 AIS Collector Starting..."
        )


        async with websockets.connect(

            AISSTREAM_URL,

            ssl=ssl_context,

            open_timeout=30,

            ping_interval=20,

            ping_timeout=60

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



        print(
            "AIS Vessels:",
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



    except Exception as e:


        print(
            "❌ AIS Collector Error:",
            e
        )



if __name__ == "__main__":


    asyncio.run(
        collect_ais()
    )
