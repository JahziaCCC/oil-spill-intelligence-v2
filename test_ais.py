from ais_correlation import (
    find_nearest_vessel,
    vessel_risk_score
)



# موقع البقعة المكتشفة من Sentinel

spill_lat = 24.3312
spill_lon = 49.894267



# بيانات تجريبية لسفن

vessels = [

    {
        "name": "Test Vessel A",
        "imo": "123456789",
        "lat": 24.35,
        "lon": 49.91,
        "speed": 8
    },


    {
        "name": "Test Vessel B",
        "imo": "987654321",
        "lat": 25.10,
        "lon": 50.50,
        "speed": 12
    }

]



nearest = find_nearest_vessel(

    spill_lat,

    spill_lon,

    vessels

)



print("================================")
print("AIS Correlation Test")
print("================================")



if nearest:


    print("🚢 Nearest Vessel")

    print("----------------")

    print(
        "Name:",
        nearest["name"]
    )

    print(
        "IMO:",
        nearest["imo"]
    )

    print(
        "Distance:",
        nearest["distance_km"],
        "km"
    )

    print(
        "Speed:",
        nearest["speed"],
        "knots"
    )


    risk = vessel_risk_score(
        nearest
    )


    print(
        "Vessel Risk Contribution:",
        risk
    )


else:

    print(
        "No vessel found nearby."
    )
