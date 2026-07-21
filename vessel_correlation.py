import math



def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371


    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)


    dlat = lat2 - lat1
    dlon = lon2 - lon1


    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(dlon / 2) ** 2
    )


    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


    return round(
        R * c,
        2
    )



def find_nearest_vessel(
    spill_lat,
    spill_lon,
    vessels,
    max_distance_km=20
):

    nearest = None

    min_distance = None


    for vessel in vessels:


        if (
            vessel.get("lat") is None
            or vessel.get("lon") is None
        ):
            continue


        distance = haversine_distance(

            spill_lat,

            spill_lon,

            vessel["lat"],

            vessel["lon"]

        )


        if distance <= max_distance_km:


            if (
                min_distance is None
                or distance < min_distance
            ):


                min_distance = distance

                nearest = vessel.copy()

                nearest["distance_km"] = distance



    return nearest



def vessel_risk_score(
    vessel
):

    if vessel is None:

        return 0



    score = 0


    distance = vessel.get(
        "distance_km",
        999
    )


    if distance < 5:

        score += 30

    elif distance < 10:

        score += 20

    else:

        score += 10



    speed = vessel.get(
        "speed",
        0
    )


    if speed > 5:

        score += 10



    return score
