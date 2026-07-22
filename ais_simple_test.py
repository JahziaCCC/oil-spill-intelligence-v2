import os
import asyncio
import websockets
import json


URL = "wss://stream.aisstream.io/v0/stream"


async def test():

    key = os.getenv("AISSTREAM_API_KEY")

    if not key:
        print("NO KEY")
        return


    msg = {
        "APIKey": key,
        "BoundingBoxes": [
            [
                [30, 10],
                [60, 35]
            ]
        ],
        "FilterMessageTypes": [
            "PositionReport"
        ]
    }


    print("Connecting...")


    async with websockets.connect(
        URL,
        open_timeout=60
    ) as ws:

        print("CONNECTED")

        await ws.send(
            json.dumps(msg)
        )

        print("SUBSCRIBED")


        for i in range(5):

            data = await ws.recv()

            print(data[:200])


asyncio.run(test())
