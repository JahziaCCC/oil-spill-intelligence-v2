import math


EARTH_RADIUS_KM = 6371.0088


def haversine(lat1, lon1, lat2, lon2):
    """
    حساب المسافة بين نقطتين على سطح الأرض (كم)
    """

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def bbox_size_km(bbox):
    """
    إرجاع عرض وارتفاع المنطقة بالكيلومتر
    bbox = [minLon, minLat, maxLon, maxLat]
    """

    min_lon, min_lat, max_lon, max_lat = bbox

    width = haversine(
        min_lat,
        min_lon,
        min_lat,
        max_lon
    )

    height = haversine(
        min_lat,
        min_lon,
        max_lat,
        min_lon
    )

    return width, height


def estimate_area_km2(area_pixels, bbox, image_shape):
    """
    حساب مساحة البقعة التقريبية بالكيلومتر المربع
    """

    width_km, height_km = bbox_size_km(bbox)

    total_area = width_km * height_km

    total_pixels = image_shape[0] * image_shape[1]

    pixel_area = total_area / total_pixels

    return area_pixels * pixel_area
