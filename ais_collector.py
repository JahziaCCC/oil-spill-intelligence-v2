import os
import asyncio
import ssl
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


async def test_ais():

    api_key = os.getenv("AISSTREAM_API_KEY")

    print(
        "AIS KEY EXISTS:",
        bool(api_key),
        "LENGTH:",
        len(api_key) if api_key else 0
    )


    if not api_key:
        print("❌ Missing API Key")
        return


    ssl_context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_CLIENT
    )

    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE


    try:

        print("📡 Connecting AISStream...")


        async with websockets.connect(

            AISSTREAM_URL,

            ssl=ssl_context,

            open_timeout=120,

            close_timeout=30,

            ping_interval=None

        ) as websocket:


            print(
                "✅ AIS Connected"
            )


            await websocket.send(
                '{"APIKey":"' + api_key + '"}'
            )


            print(
                "✅ Test message sent"
            )


    except Exception as e:

        print(
            "❌ AIS Error:",
            repr(e)
        )



if __name__ == "__main__":

    asyncio.run(
        test_ais()
    )
