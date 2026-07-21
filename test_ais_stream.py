import asyncio

from ais_stream import get_vessels



# الخليج العربي
# [minLon, minLat, maxLon, maxLat]

bbox = [

    48.0,
    23.0,
    52.0,
    27.0

]



async def main():

    print("================================")
    print("AISStream Test")
    print("================================")

    print("Connecting to AISStream...")



    vessels = await get_vessels(

        bbox,

        seconds=30

    )



    print()

    print(
        "Total Vessels:",
        len(vessels)
    )



    if vessels:


        print("\n🚢 Sample Vessels")

        print("----------------")


        for vessel in vessels[:5]:


            print(
                f"""
Name   : {vessel['name']}
MMSI   : {vessel['mmsi']}
Lat    : {vessel['lat']}
Lon    : {vessel['lon']}
Speed  : {vessel['speed']}
----------------
"""
            )


    else:

        print(
            "❌ No vessels received"
        )



if __name__ == "__main__":

    asyncio.run(
        main()
    )
