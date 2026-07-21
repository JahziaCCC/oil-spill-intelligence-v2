import os
import json
import asyncio
import ssl
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


def get_ais_key():

    key = os.getenv("AISSTREAM_API_KEY")

    if not key:
        raise ValueError(
            "AISSTREAM_API_KEY is missing"
        )

    return key



async def get_vessels(bbox, seconds=60):

    api_key = get_ais_key()

    vessels = []


    subscribe_message = {

        "APIKey": api_key,

        "BoundingBoxes": [
            [
                [
                    bbox[1],
                    bbox[0]
                ],
                [
                    bbox[3],
                    bbox[2]
                ]
            ]
        ],

        "FilterMessageTypes": [
            "PositionReport"
        ]

    }


    try:

        print(
            "Connecting AISStream..."
        )


        ssl_context = ssl.create_default_context()

        # معالجة مشكلة شهادة SSL في GitHub Runner
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE



        async with websockets.connect(

            AISSTREAM_URL,

            ssl=ssl_context,

            open_timeout=30,

            ping_interval=20,

            ping_timeout=60

        ) as websocket:



            print(
                "AISStream Connected"
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

                seconds

            ):


                try:


                    message = await asyncio.wait_for(

                        websocket.recv(),

                        timeout=10

                    )


                    data = json.loads(
                        message
                    )


                    meta = data.get(
                        "MetaData",
                        {}
                    )


                    position = (

                        data.get(
                            "Message",
                            {}
                        )
                        .get(
                            "PositionReport"
                        )

                    )



                    if position:


                        vessels.append(

                            {

                                "name":
                                meta.get(
                                    "ShipName",
                                    "Unknown"
                                ),

                                "mmsi":
                                meta.get(
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

                        )



                except asyncio.TimeoutError:

                    continue



    except Exception as e:

        print(
            "AIS Error:",
            e
        )



    return vessels
