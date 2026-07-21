def pixel_to_geo(
    pixel_x,
    pixel_y,
    bbox,
    image_shape
):
    """
    تحويل إحداثيات البكسل إلى إحداثيات جغرافية

    bbox:
    [minLon, minLat, maxLon, maxLat]

    image_shape:
    (height, width)
    """

    min_lon, min_lat, max_lon, max_lat = bbox

    height = image_shape[0]
    width = image_shape[1]


    # نسبة موقع البكسل داخل الصورة

    x_ratio = pixel_x / width

    y_ratio = pixel_y / height



    # تحويل إلى إحداثيات

    longitude = (
        min_lon +
        (x_ratio * (max_lon - min_lon))
    )


    latitude = (
        max_lat -
        (y_ratio * (max_lat - min_lat))
    )



    return {

        "latitude": round(latitude, 6),

        "longitude": round(longitude, 6)

    }
