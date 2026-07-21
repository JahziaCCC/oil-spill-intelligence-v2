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



    ssl_context = ssl.create_default_context()

    ssl_context.check_hostname = False

    ssl_context.verify_mode = ssl.CERT_NONE



    for attempt in range(1, 4):

        try:

            print(
                f"AIS Connection Attempt {attempt}/3"
            )


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


                    except asyncio.TimeoutError:

                        continue



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



                        vessel = {


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



                        vessels.append(

                            vessel

                        )



                break



        except Exception as e:


            print(

                f"AIS Attempt {attempt} Failed:",

                e

            )


            if attempt < 3:

                await asyncio.sleep(5)


            else:

                print(

                    "AIS unavailable - continue without vessels"

                )



    return vessels
