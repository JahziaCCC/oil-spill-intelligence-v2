import os
import asyncio
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

        print(
            "❌ AISSTREAM_API_KEY missing"
        )

        return



    print(
        "📡 Testing AISStream connection..."
    )


    try:

        async with websockets.connect(

            AISSTREAM_URL,

            open_timeout=60

        ) as websocket:


            print(
                "✅ WebSocket Connected"
            )


            await websocket.send(
                "{}"
            )


            print(
                "✅ Message Sent"
            )


    except Exception as e:


        print(
            "❌ AIS Connection Error:",
            e
        )



if __name__ == "__main__":

    asyncio.run(
        test_ais()
    )
