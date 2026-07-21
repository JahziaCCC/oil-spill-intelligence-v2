import math


# Sentinel-1 GRD Resolution (تقريبية)
PIXEL_SIZE_M = 10


def estimate_area_km2(area_pixels, bbox=None, image_shape=None):
    """
    حساب مساحة البقعة بالكيلومتر المربع
    باستخدام دقة Sentinel-1

    Sentinel-1 GRD:
    10m x 10m تقريباً لكل بكسل
    """

    pixel_area_m2 = PIXEL_SIZE_M * PIXEL_SIZE_M

    total_area_m2 = area_pixels * pixel_area_m2

    total_area_km2 = total_area_m2 / 1_000_000

    return round(total_area_km2, 3)



def pixel_resolution():

    """
    إرجاع دقة البكسل المستخدمة
    """

    return PIXEL_SIZE_M
