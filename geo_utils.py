def pixel_to_geo(
    x,
    y,
    bbox,
    image_shape
):
    """
    تحويل إحداثيات البكسل إلى إحداثيات جغرافية

    bbox:
    [
        min_lon,
        min_lat,
        max_lon,
        max_lat
    ]

    أو:
    [
        [min_lon, min_lat],
        [max_lon, max_lat]
    ]

    """

    height, width = image_shape[:2]


    # دعم شكلين للـ bbox
    if isinstance(bbox[0], list):

        min_lon = bbox[0][0]
        min_lat = bbox[0][1]

        max_lon = bbox[1][0]
        max_lat = bbox[1][1]

    else:

        min_lon = bbox[0]
        min_lat = bbox[1]

        max_lon = bbox[2]
        max_lat = bbox[3]



    lon = (
        min_lon
        +
        (x / width)
        *
        (max_lon - min_lon)
    )


    lat = (
        max_lat
        -
        (y / height)
        *
        (max_lat - min_lat)
    )


    return (
        round(lat, 6),
        round(lon, 6)
    )
