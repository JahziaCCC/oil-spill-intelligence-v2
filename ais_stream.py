import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


def get_ais_key():

    key = os.getenv(
        "AISSTREAM_API_KEY"
    )

    if not key:

        raise ValueError(
            "AISSTREAM_API_KEY is missing"
        )

    return key



async def get_vessels(
    bbox,
    seconds=30
):
    """
    جلب السفن القريبة من منطقة محددة

    bbox:
    [minLon,minLat,maxLon,maxLat]
    """

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

        async with websockets.connect(
            AISSTREAM_URL
        ) as websocket:


            await websocket.send(
                json.dumps(
                    subscribe_message
                )
            )



            start = asyncio.get_event_loop().time()



            while True:


                if (
                    asyncio.get_event_loop().time()
                    -
                    start
                    >
                    seconds
                ):

                    break



                message = await websocket.recv()


                data = json.loads(
                    message
                )



                meta = data.get(
                    "MetaData",
                    {}
                )


                message_data = data.get(
                    "Message",
                    {}
                )



                position = message_data.get(
                    "PositionReport",
                    {}
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
