import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


def get_ais_key():

    key = os.getenv("AISSTREAM_API_KEY")

    if not key:
        raise ValueError(
            "AISSTREAM_API_KEY is missing"
        )

    return key



async def get_vessels(
    bbox,
    seconds=60
):

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


        async with websockets.connect(

            AISSTREAM_URL,

            open_timeout=60,

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



            while True:


                elapsed = (

                    asyncio.get_event_loop().time()

                    -

                    start

                )



                if elapsed > seconds:

                    break



                try:


                    message = await asyncio.wait_for(

                        websocket.recv(),

                        timeout=10

                    )


                except asyncio.TimeoutError:

                    continue



                data = json.loads(
                    message
                )



                meta = data.get(
                    "MetaData",
                    {}
                )


                msg = data.get(
                    "Message",
                    {}
                )


                position = msg.get(
                    "PositionReport"
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



    except Exception as e:


        print(
            "AIS Error:",
            e
        )



    return vessels
